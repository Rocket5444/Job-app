# Job description extractor using Playwright sync API.
#
# This module opens a job page, tries common description selectors,
# and returns a cleaned text description.

import re

from playwright.sync_api import sync_playwright


# Clean raw text by removing excessive whitespace and repeated blank lines.
def clean_text(raw_text):
    # Replace multiple spaces/tabs with a single space.
    text = re.sub(r"[ \t]+", " ", raw_text)

    # Normalize repeated line breaks (3+ newlines -> 2 newlines).
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Trim whitespace at start/end.
    return text.strip()


# Extract job description text from a given job URL.
def extract_job_description(job_url):
    # Start with empty result in case extraction fails.
    description_text = ""

    # Start Playwright in a context manager for safe setup/cleanup.
    with sync_playwright() as p:
        # Step 1: launch Chromium browser (visible mode for beginner debugging).
        browser = p.chromium.launch(headless=False)

        # Open a new tab/page.
        page = browser.new_page()

        try:
            print("Opening job page...")
            # Step 2: open the target job URL.
            page.goto(job_url, wait_until="domcontentloaded", timeout=60000)

            # Step 3: wait for full page load.
            page.wait_for_load_state("load")
        except Exception as exc:
            # Handle navigation/load failures and return empty description.
            print(f"Error: failed to load job page ({exc}).")
            browser.close()
            return ""

        print("Extracting job description...")

        # Step 4: try common selectors that often contain job descriptions.
        selectors = [
            'div[class*="description"]',
            'div[class*="job-description"]',
            'section[class*="description"]',
        ]

        # Try each selector until text is found.
        for selector in selectors:
            try:
                locator = page.locator(selector).first
                if locator.count() > 0:
                    raw = locator.inner_text().strip()
                    if raw:
                        description_text = raw
                        break
            except Exception:
                # If one selector fails, continue trying the next.
                continue

        # Fallback: if no selector worked, use page body text as last resort.
        if not description_text:
            try:
                body_text = page.locator("body").inner_text().strip()
                if body_text:
                    description_text = body_text
            except Exception:
                pass

        # Step 7: close browser before returning.
        browser.close()

    # Error handling for missing description content.
    if not description_text:
        print("Warning: no description element/text found.")
        return ""

    # Step 6: clean text and return.
    return clean_text(description_text)
