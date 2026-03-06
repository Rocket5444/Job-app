# Simple test runner for ai_job_matcher module.

from ai_job_matcher import calculate_match_score, should_apply


# Main function keeps execution easy for beginners.
def main():
    # Sample job description text for testing.
    sample_job_description = """
    We are hiring a Data Analyst to build dashboards, analyze business data,
    create reports, and communicate insights to stakeholders.
    Experience with SQL, Python, analytics, and business intelligence is preferred.
    """

    # Calculate match score for the sample job description.
    score = calculate_match_score(sample_job_description)
    print(f"Calculated score: {score}%")

    # Print final apply/skip decision using default threshold.
    decision = should_apply(sample_job_description)
    print(f"Should apply: {decision}")


# Run test only when this file is executed directly.
if __name__ == "__main__":
    main()
