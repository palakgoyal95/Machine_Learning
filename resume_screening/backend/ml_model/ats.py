"""Transparent, job-description-aware ATS scoring utilities."""

from __future__ import annotations

import re

from .skills import extract_skills


SECTION_MARKERS = ("experience", "education", "skills", "projects", "summary", "certifications")
STOP_WORDS = {
    "about", "across", "after", "along", "applicant", "candidate", "company", "development",
    "experience", "including", "knowledge", "looking", "minimum", "must", "needed", "preferred",
    "qualifications", "required", "responsibilities", "role", "skills", "strong", "team", "their",
    "this", "using", "with", "work", "working", "years",
}


def _words(text: str) -> set[str]:
    return set(re.findall(r"[a-z][a-z0-9+#./-]{2,}", text.casefold()))


def _presentation_score(resume_text: str, skills: list[str]) -> tuple[float, dict[str, int]]:
    """Score basic ATS-readiness signals without assessing personal attributes."""
    normalized = resume_text.casefold()
    word_count = len(re.findall(r"[a-z][a-z0-9+#./-]{2,}", resume_text.casefold()))
    sections_found = sum(marker in normalized for marker in SECTION_MARKERS)
    contact_found = bool(
        re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", resume_text)
        or re.search(r"(?:linkedin\.com|github\.com|\+?\d[\d\s().-]{7,}\d)", normalized)
    )

    length_points = min(word_count / 180, 1) * 35
    section_points = min(sections_found / 4, 1) * 35
    skill_points = min(len(skills) / 6, 1) * 20
    contact_points = 10 if contact_found else 0
    return length_points + section_points + skill_points + contact_points, {
        "word_count": word_count,
        "sections_found": sections_found,
        "skills_found": len(skills),
        "contact_found": int(contact_found),
    }


def _job_keywords(job_description: str) -> set[str]:
    return {word for word in _words(job_description) if len(word) >= 4 and word not in STOP_WORDS}


def calculate_ats_score(resume_text: str, job_description: str = "") -> dict[str, object]:
    """Return a 0-100 ATS-style score and an auditable breakdown.

    When a job description is supplied, the score evaluates stated technical skills
    and meaningful keyword overlap. Without one, it reports only general resume
    readiness signals; it is deliberately not presented as a job-fit assessment.
    """
    resume_skills = extract_skills(resume_text)
    presentation, presentation_details = _presentation_score(resume_text, resume_skills)
    job_description = job_description.strip()

    if not job_description:
        return {
            "score": round(presentation),
            "has_job_description": False,
            "resume_readiness": round(presentation),
            "matched_skills": [],
            "missing_skills": [],
            "keyword_coverage": None,
            "details": presentation_details,
        }

    required_skills = extract_skills(job_description)
    matched_skills = [skill for skill in required_skills if skill in resume_skills]
    missing_skills = [skill for skill in required_skills if skill not in resume_skills]
    skill_coverage = len(matched_skills) / len(required_skills) if required_skills else None

    job_terms = _job_keywords(job_description)
    resume_terms = _words(resume_text)
    matched_terms = job_terms & resume_terms
    keyword_coverage = len(matched_terms) / len(job_terms) if job_terms else None

    weighted_parts = [(presentation, 20)]
    if skill_coverage is not None:
        weighted_parts.append((skill_coverage * 100, 55))
    if keyword_coverage is not None:
        weighted_parts.append((keyword_coverage * 100, 25))

    weight_total = sum(weight for _, weight in weighted_parts)
    score = sum(value * weight for value, weight in weighted_parts) / weight_total
    return {
        "score": round(score),
        "has_job_description": True,
        "resume_readiness": round(presentation),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "keyword_coverage": round((keyword_coverage or 0) * 100),
        "details": {
            **presentation_details,
            "required_skills": len(required_skills),
            "matched_keywords": len(matched_terms),
            "job_keywords": len(job_terms),
        },
    }
