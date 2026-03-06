# Lever ATS application automation module.
#
# This script fills common Lever application fields in a beginner-friendly way.
# It intentionally does NOT submit applications automatically.

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

from automation.human_behavior import human_scroll, human_type, random_delay


# Load resume data from resume_data.json.
def load_resume_data():
    resume_path = Path("resume_data.json")
    if not resume_path.exists():
        print("Warning: resume_data.json not found. Using empty defaults.")
        return {}

    try:
        return json.loads(resume_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Warning: failed to parse resume_data.json ({exc}).")
        return {}


# Fill a field if it exists; return True if successful.
def fill_if_exists(page, selector, value):
    try:
        if not value:
            return False
        field = page.locator(selector).first
        if field.count() == 0:
            return False
        field.scroll_into_view_if_needed()
        random_delay(0.2, 0.8)
        return human_type(page, selector, str(value))
    except Exception as exc:
        print(f"Warning: failed to fill selector '{selector}' ({exc}).")
        return False


# Main Lever apply function.
def apply_lever(job_url):
    # Load local data files used for autofill and upload.
    resume_data = load_resume_data()
    resume_pdf = Path("resume.pdf")

    # Start browser automation.
    with sync_playwright() as p:
        # Step 1 — Launch visible Chromium.
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            print("Opening Lever job page...")
            # Step 2 — Open job page.
            page.goto(job_url, wait_until="domcontentloaded", timeout=60000)
            # Step 3 — Wait for full load.
            page.wait_for_load_state("load")
        except Exception as exc:
            print(f"Error: failed to open Lever job page ({exc}).")
            browser.close()
            return False

        # Step 4 — Click apply button when present.
        apply_selectors = [
            "button:has-text('Apply for this job')",
            "a:has-text('Apply for this job')",
            "button:has-text('Apply')",
            "a:has-text('Apply')",
        ]
        clicked_apply = False
        for selector in apply_selectors:
            try:
                button = page.locator(selector).first
                if button.count() > 0:
                    button.scroll_into_view_if_needed()
                    random_delay(0.3, 1.0)
                    button.click()
                    clicked_apply = True
                    page.wait_for_timeout(1500)
                    break
            except Exception:
                pass

        if clicked_apply:
            print("Clicked apply button.")
        else:
            print("Warning: apply button not found or not clickable.")

        # Step 5 — Upload resume if file input exists.
        if resume_pdf.exists():
            print("Uploading resume...")
            upload_selectors = [
                "input[type='file']",
                "input[name*='resume']",
                "input[id*='resume']",
            ]
            uploaded = False
            for selector in upload_selectors:
                try:
                    file_input = page.locator(selector).first
                    if file_input.count() > 0:
                        file_input.set_input_files(str(resume_pdf.resolve()))
                        uploaded = True
                        break
                except Exception:
                    pass
            if not uploaded:
                print("Warning: resume upload field not found.")
        else:
            print("Warning: resume.pdf not found. Skipping upload.")

        # Step 6/7 — Fill common personal fields.
        print("Filling personal details...")
        human_scroll(page)
        name_value = resume_data.get("name", "")
        email_value = resume_data.get("email", "")
        phone_value = resume_data.get("phone", "")

        filled_name = fill_if_exists(page, "input[name*='name' i]", name_value)
        filled_email = fill_if_exists(page, "input[name*='email' i]", email_value)
        filled_phone = fill_if_exists(page, "input[name*='phone' i]", phone_value)

        if not filled_name:
            print("Warning: name field not found.")
        if not filled_email:
            print("Warning: email field not found.")
        if not filled_phone:
            print("Warning: phone field not found.")

        # Step 8 — Fill optional fields when available.
        linkedin_value = resume_data.get("linkedin", "")
        portfolio_value = resume_data.get("portfolio", "")
        website_value = resume_data.get("website", "")

        fill_if_exists(page, "input[name*='linkedin' i]", linkedin_value)
        fill_if_exists(page, "input[name*='portfolio' i]", portfolio_value)
        fill_if_exists(page, "input[name*='website' i]", website_value)

        # Step 9 — Scroll naturally to expose lazy/hidden fields.
        human_scroll(page)

        # Step 11 — Never auto-submit. Wait for manual review.
        print("Manual review mode: not submitting form automatically.")
        page.wait_for_timeout(15000)

        browser.close()

    return True
