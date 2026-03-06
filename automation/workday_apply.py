# Import json to load structured resume data from resume_data.json.
import json

# Import Path to safely work with local files like resume_data.json and resume.pdf.
from pathlib import Path

# Import Playwright sync API for beginner-friendly browser automation.
from playwright.sync_api import sync_playwright

from automation.human_behavior import human_scroll, human_type, random_delay


# Build a best-effort selector string for an input field from id/name.
def hint_selector(field):
    field_id = field.get_attribute("id") or ""
    field_name = field.get_attribute("name") or ""

    if field_id:
        return f"#{field_id}"
    if field_name:
        return f"input[name='{field_name}']"

    # Fallback selector if id/name are missing.
    return "input, textarea"


# Fill text-like fields (name/email/phone) using simple keyword matching.
def fill_text_fields(page, data):
    # Find all input and textarea elements on the page.
    fields = page.locator("input, textarea")

    # Track whether key fields were filled.
    filled_name = False
    filled_email = False
    filled_phone = False

    # Loop over each discovered field.
    for i in range(fields.count()):
        # Read one field at a time.
        field = fields.nth(i)

        # Read useful attributes that often describe a field.
        field_type = (field.get_attribute("type") or "text").lower()
        field_name = (field.get_attribute("name") or "").lower()
        field_id = (field.get_attribute("id") or "").lower()
        field_placeholder = (field.get_attribute("placeholder") or "").lower()
        aria_label = (field.get_attribute("aria-label") or "").lower()

        # Skip non-text input types.
        if field_type in {"checkbox", "radio", "file", "submit", "button", "hidden"}:
            continue

        # Combine hints so matching rules are simpler.
        hint = f"{field_name} {field_id} {field_placeholder} {aria_label}".strip()

        # Decide which value to place based on simple keyword checks.
        value = ""
        if "name" in hint:
            value = data.get("name", "")
            filled_name = bool(value)
        elif "email" in hint:
            value = data.get("email", "")
            filled_email = bool(value)
        elif "phone" in hint or "mobile" in hint or "tel" in hint:
            value = data.get("phone", "")
            filled_phone = bool(value)

        # Fill only when we found a matching value.
        if value:
            try:
                # Scroll field into view before filling to reduce visibility issues.
                field.scroll_into_view_if_needed()
                # Replace field content with the chosen value.
                # Use human-like typing instead of instant fill.
                human_type(page, hint_selector(field), value)
            except Exception as exc:
                print(f"Warning: failed to fill a text field ({exc}).")

    # Print helpful warnings if expected fields were not matched.
    if not filled_name:
        print("Warning: could not find a matching 'name' field.")
    if not filled_email:
        print("Warning: could not find a matching 'email' field.")
    if not filled_phone:
        print("Warning: could not find a matching 'phone' field.")


# Handle dropdown menus with a simple safe strategy.
def handle_dropdowns(page):
    # Find all standard <select> dropdown elements.
    dropdowns = page.locator("select")

    # Loop through each dropdown.
    for i in range(dropdowns.count()):
        dropdown = dropdowns.nth(i)
        try:
            # Scroll dropdown into view before interacting.
            dropdown.scroll_into_view_if_needed()
            # Find options inside this dropdown.
            options = dropdown.locator("option")
            # If more than one option exists, select the second option (index 1).
            if options.count() > 1:
                dropdown.select_option(index=1)
        except Exception as exc:
            print(f"Warning: failed to handle a dropdown ({exc}).")


# Handle checkboxes and radio buttons with simple safe defaults.
def handle_checkboxes(page):
    # Find all checkboxes and check the first unchecked few.
    checkboxes = page.locator("input[type='checkbox']")
    for i in range(min(checkboxes.count(), 3)):
        checkbox = checkboxes.nth(i)
        try:
            checkbox.scroll_into_view_if_needed()
            if not checkbox.is_checked():
                checkbox.check()
        except Exception as exc:
            print(f"Warning: failed to handle a checkbox ({exc}).")

    # Find radio buttons and choose the first one if present.
    radios = page.locator("input[type='radio']")
    if radios.count() > 0:
        try:
            radios.first.scroll_into_view_if_needed()
            radios.first.check()
        except Exception as exc:
            print(f"Warning: failed to handle a radio button ({exc}).")


# Main Workday apply flow.
def apply_workday(job_url):
    # Define required local file paths.
    resume_json_path = Path("resume_data.json")
    resume_pdf_path = Path("resume.pdf")

    # Ensure resume_data.json exists before starting browser work.
    if not resume_json_path.exists():
        print("Error: resume_data.json not found.")
        return False

    # Load structured candidate data from JSON.
    data = json.loads(resume_json_path.read_text(encoding="utf-8"))

    # Start Playwright in a context manager.
    with sync_playwright() as p:
        # Launch visible Chromium.
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            print("Opening job page...")
            # Open provided Workday URL.
            page.goto(job_url, wait_until="domcontentloaded", timeout=60000)
            # Wait for full load state as requested.
            page.wait_for_load_state("load")
        except Exception as exc:
            print(f"Error: failed to open job page ({exc}).")
            browser.close()
            return False

        # Try common selectors/text for an Apply button.
        print("Looking for Apply button...")
        apply_clicked = False
        apply_candidates = [
            "button:has-text('Apply')",
            "a:has-text('Apply')",
            "button:has-text('Apply Now')",
            "a:has-text('Apply Now')",
            "button[data-automation-id*='apply']",
            "a[data-automation-id*='apply']",
        ]
        for selector in apply_candidates:
            try:
                locator = page.locator(selector).first
                if locator.count() > 0:
                    locator.scroll_into_view_if_needed()
                    random_delay(0.3, 1.0)
                    locator.click()
                    apply_clicked = True
                    break
            except Exception:
                # Continue trying other selectors.
                pass

        if apply_clicked:
            print("Apply button clicked.")
            # Wait briefly for form transition.
            page.wait_for_timeout(2000)
        else:
            print("Warning: Apply button not found or could not be clicked.")

        # Try to upload resume if file and field both exist.
        if resume_pdf_path.exists():
            print("Uploading resume...")
            upload_selectors = [
                "input[type='file']",
                "input[data-automation-id*='file-upload']",
                "input[data-automation-id*='resume']",
            ]
            uploaded = False
            for selector in upload_selectors:
                try:
                    file_input = page.locator(selector).first
                    if file_input.count() > 0:
                        file_input.set_input_files(str(resume_pdf_path.resolve()))
                        uploaded = True
                        break
                except Exception:
                    pass
            if not uploaded:
                print("Warning: resume upload field not found.")
        else:
            print("Warning: resume.pdf not found. Skipping resume upload.")

        # Fill fields from resume data.
        print("Filling personal information...")
        human_scroll(page)
        fill_text_fields(page, data)

        # Handle common Workday-style controls.
        print("Handling dropdowns, checkboxes, and radio buttons...")
        handle_dropdowns(page)
        handle_checkboxes(page)

        # Scroll naturally to trigger lazy-loaded fields if any.
        human_scroll(page)

        # Do not submit. Pause for manual review.
        print("Review the form manually. Not submitting automatically.")
        page.wait_for_timeout(15000)

        # Close browser when done.
        browser.close()

    return True
