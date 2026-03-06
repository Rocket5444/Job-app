# Import sync_playwright so we can automate a browser in simple step-by-step style.
from playwright.sync_api import sync_playwright


# Create a reusable function that detects ATS platform from a job page URL.
def detect_ats(url):
    # Start with Unknown so we always return something even if no rule matches.
    detected_platform = "Unknown"

    # Start Playwright in a context manager for safe setup and cleanup.
    with sync_playwright() as p:
        # Launch Chromium in visible mode (headless=False) so beginners can watch.
        browser = p.chromium.launch(headless=False)

        # Open a new browser tab (Playwright calls this a page).
        page = browser.new_page()

        # Navigate to the target URL and wait for the first page load.
        page.goto(url)

        # Wait until the page load event fires to ensure content is available.
        page.wait_for_load_state("load")

        # Read the final current URL (some sites redirect after initial load).
        current_url = page.url.lower()

        # Read full HTML content of the loaded page for marker checks.
        html = page.content().lower()

        # ---------------------------------------------------------------
        # URL-BASED DETECTION RULES (fast checks)
        # ---------------------------------------------------------------
        if "workdayjobs" in current_url:
            detected_platform = "Workday"
        elif "greenhouse.io" in current_url:
            detected_platform = "Greenhouse"
        elif "lever.co" in current_url:
            detected_platform = "Lever"
        elif "successfactors" in current_url:
            detected_platform = "SAP SuccessFactors"

        # ---------------------------------------------------------------
        # HTML-BASED DETECTION RULES (fallback if URL was not enough)
        # These markers are common strings seen in ATS page source.
        # ---------------------------------------------------------------
        if detected_platform == "Unknown":
            if "wd5.myworkdayjobs.com" in html or "workday" in html:
                detected_platform = "Workday"
            elif "greenhouse" in html or "boards.greenhouse.io" in html:
                detected_platform = "Greenhouse"
            elif "lever" in html or "jobs.lever.co" in html:
                detected_platform = "Lever"
            elif "successfactors" in html or "sap" in html:
                detected_platform = "SAP SuccessFactors"

        # Print result so user gets immediate feedback in the terminal.
        print(f"Detected ATS platform: {detected_platform}")

        # Close browser after detection is complete.
        browser.close()

    # Return detected platform so other scripts can reuse this function.
    return detected_platform
