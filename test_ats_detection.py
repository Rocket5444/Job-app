# Import sys to read command-line input (the URL passed by the user).
import sys

# Import detect_ats from the module we created.
from ats_detector import detect_ats


# Create main() to keep script logic clean and easy to follow.
def main():
    # Validate that the user passed a URL argument.
    if len(sys.argv) < 2:
        # Show clear usage instructions for beginners.
        print("Usage: python test_ats_detection.py <job_application_url>")
        return

    # Read the URL from command-line arguments.
    url = sys.argv[1]

    # Call our detection function and store the returned ATS name.
    result = detect_ats(url)

    # Print the final result clearly.
    print(f"Final detection result: {result}")


# Run main() only when this file is executed directly.
if __name__ == "__main__":
    # Start the ATS detection test script.
    main()
