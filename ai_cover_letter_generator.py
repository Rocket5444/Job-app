# Cover letter generator module (rule-based, beginner-friendly).
#
# This module reads resume_data.json and combines resume details with
# job information to generate a tailored cover letter.

import json
from pathlib import Path


# Path to structured resume data created by resume_structurer.py.
RESUME_FILE = Path("resume_data.json")

# Output file for generated cover letter text.
OUTPUT_FILE = Path("cover_letter.txt")


# Load resume JSON safely.
def load_resume_data():
    if not RESUME_FILE.exists():
        print("Error: resume_data.json not found.")
        return {}

    try:
        return json.loads(RESUME_FILE.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Error: failed to read resume_data.json ({exc}).")
        return {}


# Helper to convert list/string sections into readable text snippets.
def section_to_text(value, fallback):
    if isinstance(value, list):
        items = [str(item).strip() for item in value if str(item).strip()]
        return ", ".join(items[:6]) if items else fallback
    if value is None:
        return fallback
    text = str(value).strip()
    return text if text else fallback


# Generate a professional cover letter from job dictionary input.
def generate_cover_letter(job):
    print("Generating cover letter...")

    # Validate job format to avoid runtime errors.
    if not isinstance(job, dict):
        print("Error: job input must be a dictionary.")
        return ""

    # Read job fields with safe defaults.
    company = str(job.get("company", "the company")).strip() or "the company"
    title = str(job.get("title", "the role")).strip() or "the role"
    description = str(job.get("description", "")).strip()

    # Step 1 — load resume information.
    resume_data = load_resume_data()

    # Extract key sections from resume data.
    name = str(resume_data.get("name", "A Candidate")).strip() or "A Candidate"
    skills_text = section_to_text(resume_data.get("skills", []), "data analysis, reporting, and communication")
    education_text = section_to_text(resume_data.get("education", []), "a relevant academic background")
    experience_text = section_to_text(resume_data.get("experience", []), "hands-on professional experience")

    # Build a short requirement hint from job description to make the letter feel tailored.
    # Keep it simple by using the first sentence-like chunk.
    requirement_hint = "your key requirements"
    if description:
        first_chunk = description.split(".")[0].strip()
        if first_chunk:
            requirement_hint = first_chunk

    # Step 2 + Step 3 — combine resume + job info into a professional letter.
    # Target length: about 150-200 words.
    cover_letter = (
        f"Dear Hiring Team at {company},\n\n"
        f"I am writing to express my interest in the {title} position at {company}. "
        f"I am excited by the opportunity to contribute my background in analytics and problem-solving to your team. "
        f"Based on the role description, I understand that success in this position involves {requirement_hint}.\n\n"
        f"My experience includes {experience_text}. In addition, I bring strengths in {skills_text}, "
        f"which I have used to support data-driven decisions, improve reporting quality, and communicate insights clearly to stakeholders. "
        f"My educational foundation includes {education_text}, which supports my practical approach to business and data challenges.\n\n"
        f"I would welcome the opportunity to discuss how my skills and experience align with your goals for this role. "
        f"Thank you for your time and consideration. I look forward to the possibility of speaking with you.\n\n"
        f"Sincerely,\n{name}"
    )

    # Step 6 — save letter to file.
    try:
        OUTPUT_FILE.write_text(cover_letter, encoding="utf-8")
        print("Cover letter created successfully.")
    except Exception as exc:
        print(f"Warning: failed to write cover_letter.txt ({exc}).")

    # Step 7 — return text.
    return cover_letter
