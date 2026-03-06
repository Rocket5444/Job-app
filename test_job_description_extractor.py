# CLI test script for job_description_extractor.

import sys

from job_description_extractor import extract_job_description


# Main function for simple command-line usage.
def main():
    # Ensure URL argument is provided.
    if len(sys.argv) < 2:
        print("Usage: python test_job_description_extractor.py <job_url>")
        return

    # Read job URL from command-line input.
    job_url = sys.argv[1]

    # Extract description text.
    description = extract_job_description(job_url)

    # Print first 500 characters (or less if shorter).
    if description:
        print("\nExtracted description preview (first 500 chars):\n")
        print(description[:500])
    else:
        print("No description extracted.")


# Run only when executed directly.
if __name__ == "__main__":
    main()
