# Import the Workday apply function from our automation module.
from automation.workday_apply import apply_workday


# Main test runner for beginners.
def main():
    # Ask user to enter a Workday job URL in terminal.
    job_url = input("Enter Workday job application URL: ").strip()

    # Check for empty input and stop with guidance.
    if not job_url:
        print("Error: URL cannot be empty.")
        return

    # Run automation and store success/failure.
    success = apply_workday(job_url)

    # Print final outcome clearly.
    if success:
        print("Workday apply test completed successfully.")
    else:
        print("Workday apply test failed. Check warnings/errors above.")


# Run main() only when this script is executed directly.
if __name__ == "__main__":
    main()
