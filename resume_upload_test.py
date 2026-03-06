# Import Path so we can build and check file paths in a beginner-friendly way.
from pathlib import Path

# Import Playwright's synchronous API so we can write simple, step-by-step code.
from playwright.sync_api import sync_playwright


# Create a main function so all script steps are grouped clearly in one place.
def main():
    # Build the full path to resume.pdf in the current project folder.
    resume_path = Path("resume.pdf").resolve()

    # Check whether resume.pdf exists before opening the browser.
    if not resume_path.exists():
        # Print a clear error message so beginners know exactly what to fix.
        print(f"Error: Could not find file: {resume_path}")
        # Explain where the file should be located.
        print("Place resume.pdf in this project directory, then run the script again.")
        # Stop the script early because upload cannot continue without the file.
        return

    # Start Playwright in a safe context manager (auto cleanup of Playwright resources).
    with sync_playwright() as p:
        # Launch Chromium in visible mode so you can watch the automation.
        browser = p.chromium.launch(headless=False)

        # Create a new browser tab (called a page in Playwright).
        page = browser.new_page()

        # Open a safe public demo site that supports file uploads.
        page.goto("https://the-internet.herokuapp.com/upload")

        # Wait until the page is fully loaded before interacting with elements.
        page.wait_for_load_state("load")

        # Find the file input element using a simple CSS selector.
        file_input = page.locator("input[type='file']")

        # Upload resume.pdf by assigning the local file path to the file input.
        file_input.set_input_files(str(resume_path))

        # Click the Upload button to submit the selected file to the demo site.
        page.locator("input[type='submit']").click()

        # Print a success message in the terminal after the upload action.
        print(f"Upload complete: {resume_path.name} was submitted successfully.")

        # Keep the browser open for 5 seconds so you can visually confirm the result.
        page.wait_for_timeout(5000)

        # Close the browser to finish the script cleanly.
        browser.close()


# Run main() only when this file is executed directly from the terminal.
if __name__ == "__main__":
    # Call the main function to start the upload test flow.
    main()
