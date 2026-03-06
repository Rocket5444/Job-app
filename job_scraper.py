# Import json so we can save scraped jobs to jobs.json.
import json

# Import Playwright sync API for straightforward browser automation.
from playwright.sync_api import sync_playwright


# Main scraper function.
def scrape_jobs():
    # This list will store all scraped job dictionaries.
    jobs = []

    # Use a set to track links we've already seen (for deduplication).
    seen_urls = set()

    # Start Playwright with automatic cleanup.
    with sync_playwright() as p:
        # Step 1: launch visible Chromium browser.
        browser = p.chromium.launch(headless=False)

        # Open a new browser tab.
        page = browser.new_page()

        try:
            print("Opening HiringCafe listings page...")
            # Step 2: open HiringCafe listings page.
            page.goto("https://hiring.cafe/", wait_until="domcontentloaded", timeout=60000)

            # Step 3: wait for page to finish loading.
            page.wait_for_load_state("load")
        except Exception as exc:
            # Basic error handling for page load failures.
            print(f"Error: failed to load HiringCafe page ({exc}).")
            browser.close()
            return []

        print("Scrolling page to load more jobs...")
        # Step 4: scroll slowly so lazy-loaded jobs can appear.
        for _ in range(12):
            page.mouse.wheel(0, 1500)
            page.wait_for_timeout(700)

        # Try several selector strategies to find job-like links/cards.
        candidate_selectors = [
            "a[href*='job']",
            "a[href*='apply']",
            "a[href*='greenhouse.io']",
            "a[href*='lever.co']",
            "a[href*='workdayjobs']",
            "article a[href]",
            "main a[href]",
        ]

        # Collect unique element handles from candidate selectors.
        handles = []
        for selector in candidate_selectors:
            try:
                handles.extend(page.query_selector_all(selector))
            except Exception:
                pass

        # Deduplicate DOM handles by href value while extracting fields.
        for handle in handles:
            try:
                # Step 5: read link, title-like text, and company-like context.
                href = handle.get_attribute("href")
                if not href:
                    continue

                # Convert relative links to absolute URL.
                absolute_url = page.url.rstrip("/") + href if href.startswith("/") else href

                # Remove duplicates by URL.
                if absolute_url in seen_urls:
                    continue

                # Try to get visible text from link first (often contains title).
                link_text = (handle.inner_text() or "").strip()

                # Attempt to infer title and company from nearby card text.
                container_text = ""
                try:
                    parent = handle.evaluate_handle("node => node.closest('article, li, div')")
                    container_text = (parent.as_element().inner_text() or "").strip() if parent else ""
                except Exception:
                    container_text = ""

                # Build simple title/company defaults.
                title = link_text if link_text else "Unknown Title"
                company = "Unknown Company"

                # If nearby text has multiple lines, use first non-empty lines as hints.
                if container_text:
                    lines = [ln.strip() for ln in container_text.splitlines() if ln.strip()]
                    if lines:
                        if title == "Unknown Title":
                            title = lines[0]
                        # Try second line as company hint when available.
                        if len(lines) > 1:
                            company = lines[1]

                # Basic safety: skip obviously empty records.
                if title == "Unknown Title" and company == "Unknown Company":
                    continue

                # Save record.
                jobs.append(
                    {
                        "company": company,
                        "title": title,
                        "url": absolute_url,
                    }
                )
                seen_urls.add(absolute_url)

            except Exception as exc:
                # Basic error handling for missing or problematic fields.
                print(f"Warning: failed to parse one listing ({exc}).")

        # Step 5/6: print how many jobs we collected.
        print(f"Collected {len(jobs)} jobs.")

        # Step 6: save to jobs.json.
        with open("jobs.json", "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)

        # Step 7: close browser.
        browser.close()

    # Return jobs list so other scripts can reuse this function.
    return jobs
