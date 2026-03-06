# Job filtering module for the application pipeline.
#
# This file helps us keep only relevant jobs before attempting automation.
# Filtering early saves time and avoids applying to roles that do not match goals.


# Main filter function.
def filter_jobs(job_list):
    # Basic error handling: input should be a list.
    if not isinstance(job_list, list):
        print("Error: filter_jobs expected a list of job dictionaries.")
        return []

    # Keywords that indicate analytics-focused roles we want.
    include_keywords = [
        "data analyst",
        "business intelligence",
        "analytics",
        "data scientist",
        "bi analyst",
    ]

    # Keywords that indicate seniority levels to avoid for this strategy.
    reject_seniority_keywords = [
        "senior",
        "lead",
        "manager",
        "director",
        "principal",
    ]

    # Keywords for unrelated technical paths to avoid.
    reject_unrelated_keywords = [
        "frontend",
        "backend",
        "devops",
        "fullstack",
    ]

    # Final list after applying all filtering rules.
    filtered_jobs = []

    # Loop through every scraped job and decide keep/reject.
    for job in job_list:
        # Basic validation for each item.
        if not isinstance(job, dict):
            continue

        # Read title safely and normalize to lowercase for keyword matching.
        title = str(job.get("title", "")).strip()
        title_lower = title.lower()

        # Skip entries with missing title.
        if not title:
            continue

        # Rule 1: keep only titles that match at least one include keyword.
        has_include_keyword = any(keyword in title_lower for keyword in include_keywords)
        if not has_include_keyword:
            continue

        # Rule 2: reject senior titles.
        has_rejected_seniority = any(keyword in title_lower for keyword in reject_seniority_keywords)
        if has_rejected_seniority:
            continue

        # Rule 3: reject unrelated technical titles.
        has_unrelated_keyword = any(keyword in title_lower for keyword in reject_unrelated_keywords)
        if has_unrelated_keyword:
            continue

        # If all rules pass, keep the job.
        filtered_jobs.append(job)

    # Print summary statistics for visibility.
    print(f"Total scraped jobs: {len(job_list)}")
    print(f"Jobs after filtering: {len(filtered_jobs)}")

    # Return filtered list for the next pipeline stage.
    return filtered_jobs
