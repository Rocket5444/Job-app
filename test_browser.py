# Import Playwright's sync API so we can write simple step-by-step Python code.
from playwright.sync_api import sync_playwright

# Create a main function so our script has a clear entry point.
def main():
    # Start Playwright inside a context manager.
    # This automatically sets up resources and cleans them up safely.
    with sync_playwright() as p:
        # Launch Chromium browser in visible mode (headless=False).
        # headless=False means you will see the browser window open.
        browser = p.chromium.launch(headless=False)

        # Open a new browser tab (called a page in Playwright).
        page = browser.new_page()

        # Navigate to the target website.
        page.goto("https://example.com")

        # Wait for 5 seconds (5000 milliseconds) so you can see the page.
        page.wait_for_timeout(5000)

        # Close the browser when done.
        browser.close()


# Run main() only when this file is executed directly.
if __name__ == "__main__":
    main()
