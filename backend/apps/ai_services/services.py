import json
import os
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

HF_API_BASE = os.getenv("HF_API_BASE", "https://api-inference.huggingface.co/models")
HF_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN", "").strip()
HF_CHAT_MODEL = os.getenv("HF_CHAT_MODEL", "google/flan-t5-large")
HF_SUGGESTION_MODEL = os.getenv("HF_SUGGESTION_MODEL", "google/flan-t5-large")

_kw_model = None
_kw_model_failed = False


def _get_kw_model():
    global _kw_model, _kw_model_failed

    if _kw_model_failed or KeyBERT is None:
        return None

    if _kw_model is None:
        try:
            _kw_model = KeyBERT()
        except Exception:
            _kw_model_failed = True
            _kw_model = None

    return _kw_model


def _normalize_hf_response(data: Any) -> str | None:
    if isinstance(data, dict):
        if data.get("error"):
            return None
        for key in ("generated_text", "summary_text", "text"):
            if isinstance(data.get(key), str):
                return data.get(key).strip()
        return None

    if isinstance(data, list) and data:
        first = data[0]
        if isinstance(first, dict):
            for key in ("generated_text", "summary_text", "text"):
                if isinstance(first.get(key), str):
                    return first.get(key).strip()
        if isinstance(first, str):
            return first.strip()

    return None


def _call_hf_inference(
    prompt: str,
    model: str,
    max_new_tokens: int = 220,
    temperature: float = 0.25,
) -> str | None:
    if not prompt.strip() or not HF_API_TOKEN:
        return None

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "return_full_text": False,
        },
    }

    try:
        response = requests.post(
            f"{HF_API_BASE.rstrip('/')}/{model}",
            headers=headers,
            json=payload,
            timeout=25,
        )
        if response.status_code == 503:
            return None
        response.raise_for_status()
        data = response.json()
    except Exception:
        return None

    return _normalize_hf_response(data)


def _extract_json_dict(text: str) -> dict[str, Any] | None:
    if not text:
        return None

    try:
        direct = json.loads(text)
        if isinstance(direct, dict):
            return direct
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        return None

    try:
        parsed = json.loads(match.group(0))
        return parsed if isinstance(parsed, dict) else None
    except Exception:
        return None


def _coerce_list(value: Any, limit: int = 3) -> list[str]:
    if isinstance(value, str):
        value = re.split(r"[\n,;|]+", value)

    if not isinstance(value, list):
        return []

    cleaned = [str(item).strip(" -") for item in value if str(item).strip()]
    return cleaned[:limit]


def parse_pdf_resume(file_obj) -> str:
    text_parts = []
    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)


def extract_keywords(text: str, limit: int = 15) -> list[str]:
    if not text:
        return []

    kw_model = _get_kw_model()
    if kw_model:
        try:
            keywords = kw_model.extract_keywords(text, top_n=limit, stop_words="english")
            return [item[0].lower() for item in keywords]
        except Exception:
            pass

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
        "project_overview": "A short description of the team project and what success looks like.",
        "description": raw_description.strip(),
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
        "qualifications": [
            "Currently pursuing or recently completed a relevant degree",
            "Portfolio or project experience that demonstrates practical skills",
            "Comfort working in a fast-moving product environment",
        ],
        "skills": keywords[:8],
    }


def _fallback_job_variants(raw_description: str, count: int) -> list[dict[str, Any]]:
    keywords = extract_keywords(raw_description, limit=18)
    base_titles = [
        "Product Engineering Intern",
        "Frontend Engineering Intern",
        "Backend Engineering Intern",
        "Full-Stack Engineering Intern",
        "AI Product Intern",
        "Data & Automation Intern",
    ]
    role_focus = [
        "ship customer-facing product improvements",
        "build polished interface experiences",
        "design stable services and APIs",
        "connect front-end and back-end workflows",
        "prototype AI-enabled product features",
        "automate operational workflows and reporting",
    ]
    qualification_sets = [
        [
            "Strong communication and collaboration skills",
            "Interest in shipping real product work",
            "Ability to work from ambiguous requirements",
        ],
        [
            "Experience with JavaScript and component-based UI development",
            "Basic understanding of responsive design and accessibility",
            "Comfort working with design systems and API integrations",
        ],
        [
            "Experience with Python or similar backend stacks",
            "Understanding of REST APIs and database concepts",
            "Ability to debug and document service behavior",
        ],
        [
            "Comfort moving across frontend and backend tasks",
            "Interest in end-to-end product delivery",
            "Ability to learn quickly and ship iteratively",
        ],
        [
            "Familiarity with AI tools or prompt-based workflows",
            "Curiosity about product experimentation and iteration",
            "Evidence of building side projects or prototypes",
        ],
        [
            "Interest in analytics, scripting, or internal tooling",
            "Ability to structure data and automate repetitive work",
            "Comfort explaining technical ideas clearly",
        ],
    ]

    drafts: list[dict[str, Any]] = []
    for index in range(count):
        template_index = index % len(base_titles)
        title = base_titles[template_index]
        focus = role_focus[template_index]
        qualification = qualification_sets[template_index]
        skill_slice = keywords[index : index + 6] or keywords[:6]

        drafts.append(
            {
                "title": title,
                "project_overview": (
                    f"Join the team to {focus} for the project described below. "
                    "You will own a scoped internship project with clear deliverables."
                ),
                "description": raw_description.strip(),
                "responsibilities": [
                    f"{focus.capitalize()} and collaborate with the core team",
                    "Translate product goals into shipped deliverables",
                    "Track progress and document implementation decisions",
                ],
                "requirements": [
                    "Ability to work from a clear project brief",
                    "Comfort with version control, reviews, and iteration",
                    "Willingness to learn and communicate blockers early",
                ],
                "qualifications": qualification,
                "skills": skill_slice or keywords[:6],
                "location": "Remote",
            }
        )

    return drafts[: max(count, 1)]


def generate_job_variants(raw_description: str, count: int = 3) -> list[dict[str, Any]]:
    count = max(1, min(int(count or 3), 8))
    keywords = extract_keywords(raw_description, limit=18)

    prompt = (
        "You are an expert hiring strategist. Generate STRICT JSON only. "
        "Return an object with one key jobs whose value is an array of full job objects. "
        "Each job object must contain title, project_overview, description, responsibilities, requirements, qualifications, skills, and location. "
        f"Generate exactly {count} distinct job drafts for the same project. "
        "Use concise but realistic internship-level language. "
        "Responsibilities, requirements, and qualifications must each be arrays of exactly 3 strings. "
        "Skills must be an array of 5 to 8 strings. "
        "Do not include markdown. "
        "\n\nPROJECT DESCRIPTION:\n"
        f"{raw_description[:5000]}\n\n"
        f"PROJECT KEYWORDS:\n{', '.join(keywords[:12])}\n"
    )
    hf_text = _call_hf_inference(
        prompt=prompt,
        model=HF_SUGGESTION_MODEL,
        max_new_tokens=900,
        temperature=0.35,
    )
    hf_payload = _extract_json_dict(hf_text or "")
    jobs: list[dict[str, Any]] = []

    if hf_payload:
        candidate_jobs = hf_payload.get("jobs")
        if isinstance(candidate_jobs, list):
            for item in candidate_jobs[:count]:
                if not isinstance(item, dict):
                    continue
                jobs.append(
                    {
                        "title": str(item.get("title", "")).strip() or "Generated Job",
                        "project_overview": str(item.get("project_overview", "")).strip(),
                        "description": str(item.get("description", raw_description)).strip(),
                        "responsibilities": _coerce_list(item.get("responsibilities"), limit=3),
                        "requirements": _coerce_list(item.get("requirements"), limit=3),
                        "qualifications": _coerce_list(item.get("qualifications"), limit=3),
                        "skills": _coerce_list(item.get("skills"), limit=8),
                        "location": str(item.get("location", "Remote")).strip() or "Remote",
                    }
                )

    if len(jobs) < count:
        fallback_jobs = _fallback_job_variants(raw_description, count)
        seen_titles = {job["title"] for job in jobs}
        for fallback in fallback_jobs:
            if len(jobs) >= count:
                break
            if fallback["title"] in seen_titles:
                continue
            jobs.append(fallback)

    return jobs[:count]


def resume_improvement_suggestions(resume_text: str, job_text: str = "") -> dict[str, Any]:
    ats = compute_ats_score(job_text, resume_text) if job_text else {"missing_keywords": []}

    suggestions = {
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
        "generation_source": "fallback",
    }

    prompt = (
        "You are an expert resume coach for internships and early-career roles. "
        "Return STRICT JSON with keys summary, project_suggestions, certifications, formatting_advice. "
        "Each list should have exactly 3 concise entries. "
        "Do not include markdown, only JSON.\n\n"
        f"RESUME:\n{resume_text[:4500]}\n\n"
        f"JOB_CONTEXT:\n{job_text[:2200]}\n"
    )
    hf_text = _call_hf_inference(
        prompt=prompt,
        model=HF_SUGGESTION_MODEL,
        max_new_tokens=320,
        temperature=0.2,
    )
    hf_payload = _extract_json_dict(hf_text or "")
    if hf_payload:
        summary = str(hf_payload.get("summary", "")).strip()
        if summary:
            suggestions["summary"] = summary[:360]

        projects = _coerce_list(hf_payload.get("project_suggestions"), limit=3)
        certifications = _coerce_list(hf_payload.get("certifications"), limit=3)
        formatting = _coerce_list(hf_payload.get("formatting_advice"), limit=3)

        if projects:
            suggestions["project_suggestions"] = projects
        if certifications:
            suggestions["certifications"] = certifications
        if formatting:
            suggestions["formatting_advice"] = formatting

        suggestions["generation_source"] = "huggingface"

    return suggestions


def simple_chat_reply(role: str, message: str) -> str:
    hf_prompt = (
        "You are CoreHire's AI hiring assistant. "
        f"The user role is '{role}'. "
        "Answer in 2 to 4 concise sentences with practical, specific advice.\n"
        f"User question: {message}"
    )
    hf_reply = _call_hf_inference(
        prompt=hf_prompt,
        model=HF_CHAT_MODEL,
        max_new_tokens=180,
        temperature=0.35,
    )
    if hf_reply:
        return hf_reply.strip().replace("\n\n", "\n")[:800]

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
