# app/matcher.py

import re
from typing import Optional
from app.skills import SKILLS_DB, SKILL_ALIASES, normalize_skill, get_skill_category


def extract_skills_from_text(text: str) -> list[str]:
    """
    Scans resume text and returns a list of recognized skills.

    Args:
        text: Cleaned resume text (from parser.py)

    Returns:
        Sorted list of unique recognized skill names
    """

    if not text:
        return []

    text_lower = text.lower()

    found_skills = set()   

    all_skills_to_check = []

    for category, skill_list in SKILLS_DB.items():
        all_skills_to_check.extend(skill_list)

    all_skills_to_check.extend(SKILL_ALIASES.keys())

    # Sort by word count descending (multi-word first), then alphabetically
    all_skills_to_check.sort(key=lambda s: (-len(s.split()), s))

    for skill in all_skills_to_check:
        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, text_lower):
            # Resolve alias to canonical name before storing
            canonical = normalize_skill(skill)
            found_skills.add(canonical)

    return sorted(list(found_skills))


def extract_skills_from_section(section_text: str) -> list[str]:
    """
    Extracts skills specifically from a skills section.

    Args:
        section_text: Text of the skills section only

    Returns:
        Sorted list of recognized skills
    """

    if not section_text:
        return []
    
    # comma, pipe, bullet (•), newline, semicolon
    # re.split with multiple delimiters
    raw_items = re.split(r'[,|\n•;\t]+', section_text)

    found_skills = set()

    for item in raw_items:
        item_clean = item.strip().lower()

        if len(item_clean) < 2:
            continue

        if item_clean.endswith(":"):
            continue

        if ":" in item_clean:
            
            item_clean = item_clean.split(":", 1)[1].strip()

        canonical = normalize_skill(item_clean)

        all_known = set()
        for skill_list in SKILLS_DB.values():
            all_known.update(skill_list)
        all_known.update(SKILL_ALIASES.keys())

        if canonical in all_known:
            found_skills.add(normalize_skill(canonical))

    # running full text scan to catch anything the section split missed
    full_scan = extract_skills_from_text(section_text)
    found_skills.update(full_scan)

    return sorted(list(found_skills))


def calculate_match(resume_skills: list[str], job_skills: list[str]) -> dict:
    """
    Compares resume skills against job description skills.

    Args:
        resume_skills: Skills extracted from the resume
        job_skills: Skills extracted from the job description

    Returns:
        Dictionary with match analysis
    """

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = resume_set & job_set

    missing = job_set - resume_set

    extra = resume_set - job_set

    # If job has no required skills, match is 100% (nothing to match against)
    if len(job_set) == 0:
        match_percentage = 100.0
    else:
        # (matched skills / total required skills) × 100
        match_percentage = round((len(matched) / len(job_set)) * 100, 2)

    # Categorize missing skills sto give targeted advice
    missing_by_category = {}
    for skill in missing:
        category = get_skill_category(skill)
        if category not in missing_by_category:
            missing_by_category[category] = []
        missing_by_category[category].append(skill)

    return {
        "match_percentage": match_percentage,
        "matched_skills": sorted(list(matched)),
        "missing_skills": sorted(list(missing)),
        "extra_skills": sorted(list(extra)),
        "missing_by_category": missing_by_category,
        "total_resume_skills": len(resume_set),
        "total_job_skills": len(job_set),
        "total_matched": len(matched)
    }