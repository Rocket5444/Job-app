# Simple CLI runner for beginners.
# This script asks for a URL, calls the central router, and prints final status.

# Import the central router function.
from job_apply_router import apply_to_job


# Main function keeps script structure clean and easy to read.
def main():
    # Ask user for a job application URL.
    job_url = input("Enter job application URL: ").strip()

    # Call the router and store success/failure.
    success = apply_to_job(job_url)

    # Print final result clearly.
    if success:
        print("Application flow completed successfully.")
    else:
        print("Application flow did not complete. See logs above.")


# Run main only when file is executed directly.
if __name__ == "__main__":
    main()
