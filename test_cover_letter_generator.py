# Test script for ai_cover_letter_generator.
#
# This script builds a sample job input, generates a cover letter,
# and prints the result to the terminal.

from ai_cover_letter_generator import generate_cover_letter


# Main test entry point.
def main():
    # Sample job data in the required format.
    sample_job = {
        "company": "Insight Analytics Inc.",
        "title": "Data Analyst",
        "description": (
            "We are looking for a Data Analyst to build dashboards, analyze operational metrics, "
            "and communicate findings to business stakeholders. "
            "Strong SQL, reporting, and collaboration skills are preferred."
        ),
    }

    # Generate cover letter text.
    cover_letter = generate_cover_letter(sample_job)

    # Print the generated letter.
    if cover_letter:
        print("\nGenerated Cover Letter:\n")
        print(cover_letter)
    else:
        print("Cover letter generation failed.")


if __name__ == "__main__":
    main()
