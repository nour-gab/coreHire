import re
from collections import Counter
from typing import Any

import pdfplumber
import requests

try:
    from keybert import KeyBERT
except Exception:
    KeyBERT = None


STOPWORDS = {
    "and",
    "the",
    "for",
    "with",
    "that",
    "this",
    "you",
    "your",
    "are",
    "our",
    "from",
    "will",
    "have",
    "has",
    "all",
}

_kw_model = KeyBERT() if KeyBERT else None


def parse_pdf_resume(file_obj) -> str:
    text_parts = []
    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)


def extract_keywords(text: str, limit: int = 15) -> list[str]:
    if not text:
        return []

    if _kw_model:
        keywords = _kw_model.extract_keywords(text, top_n=limit, stop_words="english")
        return [item[0].lower() for item in keywords]

    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{1,}", text.lower())
    filtered = [token for token in tokens if token not in STOPWORDS and len(token) > 2]
    counts = Counter(filtered)
    return [word for word, _ in counts.most_common(limit)]


def compute_ats_score(job_text: str, resume_text: str) -> dict[str, Any]:
    job_keywords = set(extract_keywords(job_text, limit=20))
    resume_keywords = set(extract_keywords(resume_text, limit=40))

    if not job_keywords:
        return {"score": 0.0, "matched_keywords": [], "missing_keywords": []}

    matched = sorted(job_keywords.intersection(resume_keywords))
    missing = sorted(job_keywords.difference(resume_keywords))
    score = round((len(matched) / len(job_keywords)) * 100, 2)

    return {
        "score": score,
        "matched_keywords": matched,
        "missing_keywords": missing,
    }


def generate_job_from_description(raw_description: str) -> dict[str, Any]:
    keywords = extract_keywords(raw_description, limit=12)
    primary = keywords[0] if keywords else "Generalist"

    return {
        "title": f"{primary.title()} Intern",
        "responsibilities": [
            "Collaborate with cross-functional teams",
            "Build features and ship improvements",
            "Document decisions and learn fast",
        ],
        "requirements": [
            "Good communication skills",
            "Basic understanding of core domain concepts",
            "Ability to learn quickly and work with feedback",
        ],
        "skills": keywords[:8],
    }


def resume_improvement_suggestions(resume_text: str, job_text: str = "") -> dict[str, Any]:
    ats = compute_ats_score(job_text, resume_text) if job_text else {"missing_keywords": []}

    return {
        "summary": "Use stronger action verbs and quantify outcomes where possible.",
        "missing_skills": ats.get("missing_keywords", [])[:8],
        "project_suggestions": [
            "Build a full-stack CRUD app with authentication",
            "Create an analytics dashboard using real-world data",
            "Automate a repetitive task with Python",
        ],
        "certifications": [
            "Google Data Analytics",
            "AWS Cloud Practitioner",
            "Meta Front-End Developer",
        ],
        "formatting_advice": [
            "Keep resume to one page for internship roles",
            "Use consistent section headings and bullet style",
            "Prioritize recent and relevant achievements",
        ],
    }


def simple_chat_reply(role: str, message: str) -> str:
    msg = message.lower()

    if role == "candidate":
        if "project" in msg:
            return "Build one role-specific project, one data project, and one automation project to show breadth."
        if "improve" in msg or "cv" in msg or "resume" in msg:
            return "Focus on quantified impact, role-specific keywords, and concise bullet points with strong verbs."
        return "Highlight measurable outcomes, tailor each resume per job, and close your skill gaps with targeted projects."

    if "description" in msg:
        return "Use outcome-oriented responsibilities and explicitly list must-have vs nice-to-have requirements."
    if "skills" in msg:
        return "Prioritize core technical skills first, then collaboration and communication competencies."
    return "Define responsibilities clearly and align requirements to real day-to-day tasks for better applicant quality."


def fetch_github_insights(github_url: str) -> dict[str, Any]:
    match = re.search(r"github\.com/([A-Za-z0-9_-]+)", github_url or "")
    if not match:
        return {"projects": [], "skills": [], "activity": {"repo_count": 0}}

    username = match.group(1)
    api_url = f"https://api.github.com/users/{username}/repos?per_page=30&sort=updated"

    try:
        response = requests.get(api_url, timeout=8)
        response.raise_for_status()
        repos = response.json()
    except Exception:
        return {"projects": [], "skills": [], "activity": {"repo_count": 0, "source": "unavailable"}}

    languages = [repo.get("language") for repo in repos if repo.get("language")]
    language_counts = Counter(languages)

    projects = [
        {
            "name": repo.get("name"),
            "description": repo.get("description") or "",
            "stars": repo.get("stargazers_count", 0),
            "updated_at": repo.get("updated_at"),
        }
        for repo in repos[:10]
    ]

    return {
        "projects": projects,
        "skills": [lang for lang, _ in language_counts.most_common(8)],
        "activity": {"repo_count": len(repos), "source": "github"},
    }


def parse_linkedin_profile_simulation(raw_text: str) -> dict[str, Any]:
    skills = extract_keywords(raw_text, limit=10)
    return {
        "headline": "Imported LinkedIn profile (simulation)",
        "skills": skills,
        "activity": "Parsed manually provided profile text",
    }
