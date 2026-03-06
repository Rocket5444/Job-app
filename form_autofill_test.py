# Import json so we can read structured resume data from resume_data.json.
import json

# Import Path so we can safely check if files exist.
from pathlib import Path

# Import Playwright sync API for simple step-by-step browser automation.
from playwright.sync_api import sync_playwright


# Create a helper function that decides which resume value to use for a text field.
def get_value_for_field(field_hint, resume_data):
    # Convert field hint text to lowercase to make matching easier.
    hint = (field_hint or "").lower()

    # If a field hint contains "name", return the resume name.
    if "name" in hint:
        return resume_data.get("name", "")

    # If a field hint contains "email", return the resume email.
    if "email" in hint:
        return resume_data.get("email", "")

    # If a field hint contains "phone", return the resume phone.
    if "phone" in hint or "mobile" in hint or "tel" in hint:
        return resume_data.get("phone", "")

    # If no rule matches, return empty string.
    return ""


# Create a main function to keep all steps organized.
def main():
    # Define the path to the JSON file created by your previous script.
    data_path = Path("resume_data.json")

    # Stop early if resume_data.json is missing.
    if not data_path.exists():
        print("Error: 'resume_data.json' was not found in this folder.")
        print("Please generate resume_data.json first, then run this script again.")
        return

    # Load the JSON data from file into a Python dictionary.
    resume_data = json.loads(data_path.read_text(encoding="utf-8"))

    # Start Playwright safely with automatic cleanup.
    with sync_playwright() as p:
        # Launch Chromium in visible mode so you can watch each action.
        browser = p.chromium.launch(headless=False)

        # Open a new browser tab (called a page).
        page = browser.new_page()

        # Open a safe public demo form page from Selenium's official test site.
        page.goto("https://www.selenium.dev/selenium/web/web-form.html")

        # Wait until page is fully loaded before we interact with fields.
        page.wait_for_load_state("load")

        # Keep track of whether important fields were found and filled.
        filled_name = False
        filled_email = False
        filled_phone = False

        # --------------------------------------------------------------------
        # SELECTORS EXPLANATION:
        # A selector is a text pattern that tells Playwright how to find elements.
        # Example below: "input, textarea" means "find all input and textarea tags".
        # --------------------------------------------------------------------
        fields = page.locator("input, textarea")

        # Loop through every field so we can fill matching ones automatically.
        for i in range(fields.count()):
            # Get one field at a time using its index.
            field = fields.nth(i)

            # Read useful attributes that help identify the field's purpose.
            field_type = (field.get_attribute("type") or "text").lower()
            field_name = field.get_attribute("name") or ""
            field_id = field.get_attribute("id") or ""
            field_placeholder = field.get_attribute("placeholder") or ""

            # Combine hints so we can match keywords like name/email/phone.
            combined_hint = f"{field_name} {field_id} {field_placeholder}".strip()

            # Skip non-textual input types for this matching step.
            if field_type in {"radio", "checkbox", "submit", "button", "file", "hidden"}:
                continue

            # Decide what value to fill based on the field hint.
            value = get_value_for_field(combined_hint, resume_data)

            # If we have a matching value, fill the field.
            if value:
                # ----------------------------------------------------------------
                # page.fill() explanation:
                # page.fill(selector, value) or locator.fill(value) puts text into
                # text-like fields and replaces existing text.
                # ----------------------------------------------------------------
                field.fill(value)

                # Track which core field got filled.
                hint_lower = combined_hint.lower()
                if "name" in hint_lower:
                    filled_name = True
                elif "email" in hint_lower:
                    filled_email = True
                elif "phone" in hint_lower or "mobile" in hint_lower or "tel" in hint_lower:
                    filled_phone = True

        # --------------------------------------------------------------------
        # page.select_option() explanation:
        # This chooses an option in a <select> dropdown.
        # Here we pick the second option when available (index 1), to show usage.
        # --------------------------------------------------------------------
        dropdowns = page.locator("select")
        for i in range(dropdowns.count()):
            dropdown = dropdowns.nth(i)
            options = dropdown.locator("option")
            if options.count() > 1:
                dropdown.select_option(index=1)

        # Find radio buttons and check the first one if any exist.
        radios = page.locator("input[type='radio']")
        if radios.count() > 0:
            radios.first.check()

        # --------------------------------------------------------------------
        # page.check() explanation:
        # page.check(selector) or locator.check() marks a checkbox/radio as checked.
        # It is safer than clicking because it ensures checked state.
        # --------------------------------------------------------------------
        checkboxes = page.locator("input[type='checkbox']")
        if checkboxes.count() > 0:
            checkboxes.first.check()

        # Warn the user if expected text fields were not detected.
        if not filled_name:
            print("Warning: No form field matched for name.")
        if not filled_email:
            print("Warning: No form field matched for email.")
        if not filled_phone:
            print("Warning: No form field matched for phone.")

        # Print confirmation that autofill steps are complete.
        print("Autofill completed. Review the form in the browser window now.")

        # Do NOT submit the form. Wait 10 seconds for manual review.
        page.wait_for_timeout(10000)

        # Close browser after review time.
        browser.close()


# Run main() only when this file is executed directly.
if __name__ == "__main__":
    # Start the form autofill test.
    main()
