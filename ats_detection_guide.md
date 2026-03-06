# ATS Detection Guide (Beginner-Friendly)

## What is an ATS platform?

ATS means **Applicant Tracking System**.
Companies use ATS platforms to publish jobs, collect applications, and manage candidates.

Common ATS platforms include:
- Workday
- Greenhouse
- Lever
- SAP SuccessFactors

---

## Why detect ATS platforms?

When building job-application automation, each ATS site has different page structure.
If you know the ATS platform first, you can apply the right automation steps for that platform.

Example:
- If page is Workday, use Workday-specific selectors and workflow.
- If page is Greenhouse, use Greenhouse-specific selectors.

---

## How the detection logic works in this project

The script uses two simple checks:

1. **URL keyword checks**
   - `workdayjobs` -> Workday
   - `greenhouse.io` -> Greenhouse
   - `lever.co` -> Lever
   - `successfactors` -> SAP SuccessFactors

2. **HTML marker checks** (fallback)
   - If URL is unclear, script scans page HTML for known platform markers.

If nothing matches, result is **Unknown**.

---

## Files added

- `ats_detector.py`
  - Contains function `detect_ats(url)`.
- `test_ats_detection.py`
  - Small test runner script that accepts a URL and prints result.

---

## How to run

Make sure your virtual environment is active and Playwright is installed.

Run:

```bash
python test_ats_detection.py "https://boards.greenhouse.io/examplecompany/jobs/123456"
```

You should see output like:

```text
Detected ATS platform: Greenhouse
Final detection result: Greenhouse
```

---

## Notes

- Browser opens in visible mode (`headless=False`) so you can observe behavior.
- This version is intentionally simple and beginner-friendly (rule-based only, no AI).
