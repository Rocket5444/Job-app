# Beginner-friendly script to run the full auto-apply flow.
# Flow: scrape_jobs() -> filter_jobs() -> process_jobs()

from job_application_pipeline import run_pipeline


# Script entry point.
def main():
    print("Starting auto-apply pipeline...")

    # Run full pipeline and get summary stats.
    stats = run_pipeline()

    # Print final outcome clearly.
    print("\nAuto-apply run complete.")
    print(f"Attempted: {stats.get('attempted', 0)}")
    print(f"Successful: {stats.get('successful', 0)}")


if __name__ == "__main__":
    main()
