"""
Pytest suite for app/ai.py
Tests pure logic only — no real API calls.
Run with: pytest tests/test_ai.py -v
"""

import pytest
import os


class TestBuildPrompt:

    def setup_method(self):
        from app.ai import build_prompt
        self.build_prompt = build_prompt
        self.fake_match = {
            "match_percentage": 50.0,
            "matched_skills": ["python", "git"],
            "missing_skills": ["docker", "fastapi"],
            "missing_by_category": {
                "devops": ["docker"],
                "web_frameworks": ["fastapi"]
            },
            "extra_skills": ["unity"]
        }

    def test_returns_a_string(self):
        result = self.build_prompt("resume text", "job description", self.fake_match)
        assert isinstance(result, str)

    def test_prompt_contains_resume_text(self):
        result = self.build_prompt("John Doe Python Developer", "some JD", self.fake_match)
        assert "John Doe Python Developer" in result

    def test_prompt_contains_job_description(self):
        result = self.build_prompt("some resume", "Looking for FastAPI developer", self.fake_match)
        assert "Looking for FastAPI developer" in result

    def test_prompt_contains_match_percentage(self):
        result = self.build_prompt("resume", "jd", self.fake_match)
        assert "50.0%" in result

    def test_prompt_contains_missing_skills(self):
        result = self.build_prompt("resume", "jd", self.fake_match)
        assert "docker" in result
        assert "fastapi" in result

    def test_prompt_is_substantial_length(self):
        result = self.build_prompt("resume", "jd", self.fake_match)
        assert len(result) > 200


class TestGetAiSuggestionsNoKey:

    def test_missing_api_key_returns_error_dict_not_exception(self):
        """
        Confirms a missing key causes graceful error return,
        NOT an unhandled exception that crashes the caller.
        """
        from app.ai import get_ai_suggestions

        # Point to a port nothing is listening on
        original_url = os.environ.get("OLLAMA_BASE_URL")
        os.environ["OLLAMA_BASE_URL"] = "http://localhost:9999/v1"

        try:
            result = get_ai_suggestions(
                resume_text="resume",
                job_description="jd",
                match_result={
                    "match_percentage": 0,
                    "matched_skills": [],
                    "missing_skills": [],
                    "missing_by_category": {},
                    "extra_skills": []
                }
            )

            assert isinstance(result, dict)
            assert result["success"] is False
            assert result["suggestions"] is None
            assert result["error"] is not None

        finally:
            if original_url:
                os.environ["OLLAMA_BASE_URL"] = original_url
            else:
                os.environ.pop("OLLAMA_BASE_URL", None)