# Greenhouse ATS automation module (beginner-friendly placeholder implementation).
#
# This module demonstrates how to use human behavior helpers for Greenhouse forms.
# It does not auto-submit applications.

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

from automation.human_behavior import human_scroll, human_type, random_delay


# Load structured profile data.
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


# Fill a field using human typing if selector exists.
def fill_if_exists(page, selector, value):
    if not value:
        return False
    try:
        field = page.locator(selector).first
        if field.count() == 0:
            return False
        field.scroll_into_view_if_needed()
        random_delay(0.2, 0.7)
        return human_type(page, selector, str(value))
    except Exception as exc:
        print(f"Warning: failed to fill '{selector}' ({exc}).")
        return False


# Apply flow for Greenhouse pages.
def apply_greenhouse(job_url):
    data = load_resume_data()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            print("Opening Greenhouse job page...")
            page.goto(job_url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_load_state("load")
        except Exception as exc:
            print(f"Error: failed to open Greenhouse page ({exc}).")
            browser.close()
            return False

        human_scroll(page)

        # Try fill common fields.
        fill_if_exists(page, "input[name*='name' i]", data.get("name", ""))
        fill_if_exists(page, "input[name*='email' i]", data.get("email", ""))
        fill_if_exists(page, "input[name*='phone' i]", data.get("phone", ""))

        print("Manual review mode: not submitting form automatically.")
        page.wait_for_timeout(15000)
        browser.close()

    return True
