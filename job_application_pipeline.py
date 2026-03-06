# Central pipeline for job scraping -> filtering -> smart decision -> applying.

# Import scraper stage.
from job_scraper import scrape_jobs

# Import filter stage.
from job_filter import filter_jobs

# Import smart decision engine (AI matching + conditional apply).
from smart_apply_engine import evaluate_and_apply

# Import database helpers to persist applied job records.
from database.job_database import (
    check_if_applied,
    initialize_database,
    insert_application,
)


# Process job applications one by one.
def process_jobs(job_list):
    # Basic input validation.
    if not isinstance(job_list, list):
        print("Error: process_jobs expected a list.")
        return {"attempted": 0, "successful": 0, "skipped": 0}

    attempted = 0
    successful = 0
    skipped = 0

    # Loop through each filtered job and run smart evaluation.
    for job in job_list:
        if not isinstance(job, dict):
            continue

        job_url = job.get("url", "")
        title = job.get("title", "Unknown Title")
        company = job.get("company", "Unknown Company")

        # Skip records with no URL.
        if not job_url:
            print(f"Skipping job with missing URL: {company} - {title}")
            skipped += 1
            continue

        # Check DB first. If already applied, skip this job.
        if check_if_applied(job_url):
            print(f"Skipping already-applied job: {company} - {title}")
            skipped += 1
            continue

        attempted += 1
        print(f"\nProcessing job {attempted}: {company} - {title}")

        try:
            # Use smart decision engine instead of direct router calls.
            result = evaluate_and_apply(job)
            decision = result.get("decision", "skip")

            if decision == "apply":
                successful += 1
                status = "applied"
            elif decision == "apply_failed":
                status = "failed"
            else:
                status = "skipped"

            # Store outcome in SQLite database.
            insert_application(company, title, job_url, status)

        except Exception as exc:
            # Continue even if one job fails.
            print(f"Warning: failed to process job URL '{job_url}' ({exc}).")
            # Persist failure outcome for traceability.
            insert_application(company, title, job_url, "error")

    return {"attempted": attempted, "successful": successful, "skipped": skipped}


# Pipeline entry function.
def run_pipeline():
    # Ensure DB/table exists every time pipeline starts.
    initialize_database()

    # Step 1: scrape.
    scraped_jobs = scrape_jobs()

    # Step 2: filter.
    filtered_jobs = filter_jobs(scraped_jobs)

    # Step 3: smart evaluate/apply.
    stats = process_jobs(filtered_jobs)

    print("\nPipeline summary:")
    print(f"Attempted applications: {stats['attempted']}")
    print(f"Successful automation runs: {stats['successful']}")
    print(f"Skipped jobs: {stats['skipped']}")

    return stats
