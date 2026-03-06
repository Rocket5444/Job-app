# Central router for job application automation.
#
# Why this file exists:
# Different ATS platforms (Workday, Greenhouse, Lever, etc.) have different page
# layouts and workflows. Instead of writing one huge script for every platform,
# we detect the platform first and then route to the correct automation engine.
#
# This keeps the project modular:
# - ATS detection logic lives in ats_detector.py
# - Platform-specific automation lives in separate modules (for example Workday)
# - This router connects both parts in one simple entry point

# Import URL parsing helpers for basic input validation.
from urllib.parse import urlparse

# Import ATS detector so we can identify platform from a job URL.
from ats_detector import detect_ats

# Import Workday automation engine.
from automation.workday_apply import apply_workday
from automation.lever_apply import apply_lever


# Validate that the provided URL looks like a real web URL.
def is_valid_url(job_url):
    # Empty values are invalid.
    if not job_url:
        return False

    # Parse URL into components (scheme, host, path, etc.).
    parsed = urlparse(job_url)

    # A valid web URL should have scheme (http/https) and host (netloc).
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


# Main router function used by the rest of the project.
def apply_to_job(job_url):
    # Step 1: start message.
    print("Starting application process...")

    # Validate URL early to avoid confusing browser/runtime errors later.
    if not is_valid_url(job_url):
        print("Error: Invalid URL. Please provide a full URL like https://example.com/job")
        return False

    # Step 2: detect ATS platform.
    print("Detecting ATS platform...")
    try:
        ats_platform = detect_ats(job_url)
    except Exception as exc:
        # Basic error handling for detection failures.
        print(f"Error: ATS detection failed ({exc}).")
        return False

    # Show detected platform so users understand routing decision.
    print(f"Detected platform: {ats_platform}")

    # Step 3: route to platform-specific engine.
    if ats_platform == "Workday":
        print("Routing to Workday automation...")
        return apply_workday(job_url)

    if ats_platform == "Greenhouse":
        print("Greenhouse automation not implemented yet")
        return False

    if ats_platform == "Lever":
        print("Routing to Lever automation...")
        return apply_lever(job_url)

    # Covers SAP SuccessFactors and any other unsupported/unknown platforms for now.
    print("Unsupported platform")
    return False
