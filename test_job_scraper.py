# Import scraper function from job_scraper module.
from job_scraper import scrape_jobs


# Simple test runner.
def main():
    # Run scraper and store results.
    jobs = scrape_jobs()

    # Print first 5 jobs so user can quickly inspect output.
    print("\nFirst 5 jobs:")
    for index, job in enumerate(jobs[:5], start=1):
        print(f"{index}. {job}")


# Run only when executed directly.
if __name__ == "__main__":
    main()
