"""
Pytest test suite for app/skills.py
Run with: pytest tests/test_skills.py -v
"""

import pytest
from app.skills import SKILLS_DB, get_all_skills, normalize_skill, get_skill_category


class TestGetAllSkills:
    """Group related tests in a class — pytest convention"""

    def test_returns_a_set(self):
        result = get_all_skills()
        assert isinstance(result, set)

    def test_contains_known_skills(self):
        result = get_all_skills()
        assert "python" in result
        assert "docker" in result

    def test_contains_aliases(self):
        result = get_all_skills()
        assert "js" in result
        assert "k8s" in result


class TestNormalizeSkill:

    def test_lowercases_input(self):
        assert normalize_skill("Python") == "python"

    def test_strips_whitespace(self):
        assert normalize_skill("  javascript  ") == "javascript"

    def test_resolves_alias(self):
        assert normalize_skill("js") == "javascript"
        assert normalize_skill("k8s") == "kubernetes"

    def test_unknown_skill_passes_through(self):
        assert normalize_skill("some_random_thing") == "some_random_thing"


class TestGetSkillCategory:

    @pytest.mark.parametrize("skill,expected_category", [
        ("python", "languages"),
        ("docker", "devops"),
        ("react", "web_frameworks"),
        ("mongodb", "databases"),
        ("js", "languages"),       # tests alias resolution inside categorization
    ])
    def test_known_skill_categories(self, skill, expected_category):
        assert get_skill_category(skill) == expected_category

    def test_unknown_skill_returns_other(self):
        assert get_skill_category("nonexistent_skill_xyz") == "other"

    class TestSkillsDBIntegrity:

      def test_no_skill_appears_in_multiple_categories(self):
        seen = {}
        duplicates = []
        for category, skills in SKILLS_DB.items():
            for skill in skills:
                if skill in seen:
                    duplicates.append((skill, seen[skill], category))
                seen[skill] = category
        assert duplicates == [], f"Duplicate skills found: {duplicates}"