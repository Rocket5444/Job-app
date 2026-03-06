# AI-style job matcher using simple NLP (TF-IDF + cosine similarity).
#
# Install dependency first:
#   pip install scikit-learn
#
# This module compares resume text with a job description and returns
# a match score from 0 to 100.

import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# File that contains structured resume information.
RESUME_FILE = Path("resume_data.json")


# Load resume JSON data safely.
def load_resume_data():
    if not RESUME_FILE.exists():
        print("Error: resume_data.json not found.")
        return {}

    try:
        return json.loads(RESUME_FILE.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Error: failed to read resume_data.json ({exc}).")
        return {}


# Combine resume sections into one text block.
def build_resume_text(resume_data):
    # Pull section fields safely, using empty defaults.
    skills = resume_data.get("skills", [])
    education = resume_data.get("education", [])
    experience = resume_data.get("experience", [])

    # Convert list sections to plain text if needed.
    if isinstance(skills, list):
        skills_text = " ".join(str(item) for item in skills)
    else:
        skills_text = str(skills)

    if isinstance(education, list):
        education_text = " ".join(str(item) for item in education)
    else:
        education_text = str(education)

    if isinstance(experience, list):
        experience_text = " ".join(str(item) for item in experience)
    else:
        experience_text = str(experience)

    # Final combined resume text used for NLP comparison.
    return f"{skills_text} {education_text} {experience_text}".strip()


# Calculate match score between resume text and one job description.
def calculate_match_score(job_description):
    # Basic validation for description input.
    if not job_description or not str(job_description).strip():
        print("Warning: empty job description provided.")
        return 0.0

    # Load and combine resume data.
    resume_data = load_resume_data()
    resume_text = build_resume_text(resume_data)

    if not resume_text:
        print("Warning: resume text is empty, score will be 0.")
        return 0.0

    # -----------------------------------------------------------------
    # TF-IDF explanation:
    # TF-IDF turns text into numbers based on word importance.
    # - TF (term frequency): how often a word appears in a text.
    # - IDF (inverse document frequency): gives less weight to very common words.
    # This helps compare resume text and job description meaningfully.
    # -----------------------------------------------------------------
    vectorizer = TfidfVectorizer(stop_words="english")

    # Fit on both texts and convert them into vectors.
    vectors = vectorizer.fit_transform([resume_text, str(job_description)])

    # -----------------------------------------------------------------
    # Cosine similarity explanation:
    # Measures angle between vectors (how similar direction is).
    # Value is between 0 and 1:
    # - 1 means very similar
    # - 0 means very different
    # We convert to percentage (0 to 100).
    # -----------------------------------------------------------------
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    score = float(similarity * 100)

    return round(score, 2)


# Decide whether to apply based on match score threshold.
def should_apply(job_description, threshold=60.0):
    score = calculate_match_score(job_description)

    print(f"Match score: {score}%")

    if score >= threshold:
        print("Decision: Apply")
        return True

    print("Decision: Skip")
    return False
