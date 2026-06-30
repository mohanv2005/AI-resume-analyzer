# tests/test_matcher.py
"""
Pytest suite for app/matcher.py
Run with: pytest tests/test_matcher.py -v
"""

import pytest
from app.matcher import (
    extract_skills_from_text,
    extract_skills_from_section,
    calculate_match
)


class TestExtractSkillsFromText:

    def test_empty_text_returns_empty_list(self):
        assert extract_skills_from_text("") == []

    def test_none_like_input_returns_empty_list(self):
        # extract_skills_from_text checks `if not text`, so None should also work
        assert extract_skills_from_text(None) == []

    def test_finds_single_skill(self):
        result = extract_skills_from_text("I am a Python developer")
        assert "python" in result

    def test_finds_multiple_skills(self):
        text = "Experienced in Python, FastAPI, and Docker"
        result = extract_skills_from_text(text)
        assert "python" in result
        assert "fastapi" in result
        assert "docker" in result

    def test_resolves_alias_in_text(self):
        # "js" should resolve to "javascript"
        result = extract_skills_from_text("I know js and ts well")
        assert "javascript" in result
        assert "typescript" in result

    def test_no_duplicate_skills(self):
        # Mentioning python twice should still return it once (it's a set)
        text = "Python developer. I love Python."
        result = extract_skills_from_text(text)
        assert result.count("python") == 1

    def test_avoids_substring_false_positive(self):
        # "c" should NOT match inside "docker" or "javascript"
        # word boundary \b should prevent this
        text = "I use Docker and JavaScript daily"
        result = extract_skills_from_text(text)
        # "c" as a standalone skill should not appear just because
        # it's a substring of docker/javascript
        assert "c" not in result

    def test_multiword_skill_detected(self):
        text = "I have experience in machine learning and deep learning"
        result = extract_skills_from_text(text)
        assert "machine learning" in result
        assert "deep learning" in result


class TestExtractSkillsFromSection:

    def test_empty_section_returns_empty_list(self):
        assert extract_skills_from_section("") == []

    def test_comma_separated_skills(self):
        section = "Python, FastAPI, SQL, Docker"
        result = extract_skills_from_section(section)
        assert "python" in result
        assert "fastapi" in result
        assert "sql" in result
        assert "docker" in result

    def test_handles_category_labels(self):
        # Mirrors your actual resume's skills section format
        section = "Languages: Python, JavaScript, C#\nTools: Git, Unity"
        result = extract_skills_from_section(section)
        assert "python" in result
        assert "javascript" in result
        assert "c#" in result
        assert "git" in result
        assert "unity" in result

    def test_bullet_separated_skills(self):
        section = "Python\n• FastAPI\n• Docker"
        result = extract_skills_from_section(section)
        assert "python" in result
        assert "fastapi" in result
        assert "docker" in result


class TestCalculateMatch:

    def test_perfect_match(self):
        resume = ["python", "fastapi", "sql"]
        job = ["python", "fastapi", "sql"]
        result = calculate_match(resume, job)
        assert result["match_percentage"] == 100.0
        assert result["missing_skills"] == []

    def test_no_match(self):
        resume = ["python", "fastapi"]
        job = ["java", "spring"]
        result = calculate_match(resume, job)
        assert result["match_percentage"] == 0.0
        assert set(result["missing_skills"]) == {"java", "spring"}

    def test_partial_match(self):
        resume = ["python", "fastapi", "sql"]
        job = ["python", "fastapi", "docker", "kubernetes"]
        result = calculate_match(resume, job)
        # 2 matched out of 4 required = 50%
        assert result["match_percentage"] == 50.0
        assert set(result["matched_skills"]) == {"python", "fastapi"}
        assert set(result["missing_skills"]) == {"docker", "kubernetes"}

    def test_extra_skills_detected(self):
        resume = ["python", "fastapi", "sql", "git"]
        job = ["python", "fastapi"]
        result = calculate_match(resume, job)
        assert set(result["extra_skills"]) == {"sql", "git"}

    def test_empty_job_skills_gives_full_match(self):
        # No requirements = nothing to fail, so 100%
        resume = ["python", "sql"]
        job = []
        result = calculate_match(resume, job)
        assert result["match_percentage"] == 100.0

    def test_empty_resume_skills(self):
        resume = []
        job = ["python", "sql"]
        result = calculate_match(resume, job)
        assert result["match_percentage"] == 0.0
        assert set(result["missing_skills"]) == {"python", "sql"}

    def test_missing_by_category_groups_correctly(self):
        resume = ["python"]
        job = ["python", "docker", "kubernetes", "react"]
        result = calculate_match(resume, job)
        # docker and kubernetes are "devops", react is "web_frameworks"
        assert "devops" in result["missing_by_category"]
        assert set(result["missing_by_category"]["devops"]) == {"docker", "kubernetes"}
        assert "web_frameworks" in result["missing_by_category"]
        assert "react" in result["missing_by_category"]["web_frameworks"]

    def test_counts_are_correct(self):
        resume = ["python", "fastapi", "sql"]
        job = ["python", "fastapi", "docker"]
        result = calculate_match(resume, job)
        assert result["total_resume_skills"] == 3
        assert result["total_job_skills"] == 3
        assert result["total_matched"] == 2