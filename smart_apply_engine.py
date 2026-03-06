# Smart apply decision engine.
#
# Purpose:
# 1) Extract job description text from the job page
# 2) Calculate AI match score between resume and job description
# 3) Decide whether to apply based on a threshold
# 4) Route high-match jobs to ATS-specific automation

# Import description extractor.
from job_description_extractor import extract_job_description

# Import AI matcher score function.
from ai_job_matcher import calculate_match_score

# Import ATS router that knows how to apply by platform.
from job_apply_router import apply_to_job


# Evaluate one job and apply only when match score is high enough.
def evaluate_and_apply(job, threshold=60.0):
    # Validate input shape so the function fails safely.
    if not isinstance(job, dict):
        print("Error: evaluate_and_apply expected a job dictionary.")
        return {"decision": "skip", "score": 0.0, "reason": "invalid_job_format"}

    # Read job fields with beginner-friendly defaults.
    company = job.get("company", "Unknown Company")
    title = job.get("title", "Unknown Title")
    job_url = job.get("url", "")

    # Step 1 — print context for this job.
    print(f"\nEvaluating job: {company} - {title}")

    # Validate URL before any browser work.
    if not job_url:
        print("Error: job URL is missing.")
        return {"decision": "skip", "score": 0.0, "reason": "missing_url"}

    # Step 2 — extract job description.
    print("Extracting job description...")
    try:
        description = extract_job_description(job_url)
    except Exception as exc:
        # Error handling so extractor failures do not crash the pipeline.
        print(f"Warning: failed to extract description ({exc}).")
        return {"decision": "skip", "score": 0.0, "reason": "extraction_failed"}

    # If extraction returned empty text, skip safely.
    if not description:
        print("Warning: description is empty. Skipping job.")
        return {"decision": "skip", "score": 0.0, "reason": "empty_description"}

    # Step 3 — send description to AI matcher.
    print("Calculating AI match score...")
    score = calculate_match_score(description)

    # Step 4 — print score.
    print(f"AI match score: {score}%")

    # Step 5/6/7 — compare with threshold and decide.
    if score >= threshold:
        print("High match job detected")
        print("Decision: Apply")
        applied_ok = apply_to_job(job_url)
        return {
            "decision": "apply" if applied_ok else "apply_failed",
            "score": score,
            "reason": "high_match",
        }

    print("Job skipped due to low match")
    print("Decision: Skip")
    return {"decision": "skip", "score": score, "reason": "low_match"}
