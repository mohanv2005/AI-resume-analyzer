"""
Pytest suite for app/providers/
Tests provider factory and base interface.
Real API calls are not made — providers without keys
are tested for graceful error handling only.
Run with: pytest tests/test_providers.py -v
"""

import pytest
import os
from app.providers.base import BaseProvider
from app.providers.factory import get_provider, SUPPORTED_PROVIDERS


class TestBaseProvider:

    def test_generate_raises_not_implemented(self):
        provider = BaseProvider()
        with pytest.raises(NotImplementedError):
            provider.generate("test prompt")

    def test_get_provider_name_returns_class_name(self):
        provider = BaseProvider()
        assert provider.get_provider_name() == "BaseProvider"


class TestProviderFactory:

    def test_returns_ollama_provider(self):
        from app.providers.ollama import OllamaProvider
        os.environ["AI_PROVIDER"] = "ollama"
        provider = get_provider()
        assert isinstance(provider, OllamaProvider)

    def test_unknown_provider_raises_value_error(self):
        os.environ["AI_PROVIDER"] = "unknown_provider"
        with pytest.raises(ValueError) as exc_info:
            get_provider()
        assert "Unknown AI provider" in str(exc_info.value)

    def test_supported_providers_list_is_complete(self):
        expected = ["ollama", "openrouter", "openai", "gemini", "claude"]
        assert set(SUPPORTED_PROVIDERS) == set(expected)

    def test_provider_name_is_case_insensitive(self):
        from app.providers.ollama import OllamaProvider
        os.environ["AI_PROVIDER"] = "OLLAMA"
        provider = get_provider()
        assert isinstance(provider, OllamaProvider)


class TestOllamaProvider:

    def test_initializes_with_default_values(self):
        from app.providers.ollama import OllamaProvider
        os.environ.pop("OLLAMA_MODEL", None)
        provider = OllamaProvider()
        assert provider.model == "llama3.2:3b"

    def test_reads_model_from_env(self):
        from app.providers.ollama import OllamaProvider
        os.environ["OLLAMA_MODEL"] = "llama3.2:1b"
        provider = OllamaProvider()
        assert provider.model == "llama3.2:1b"
        os.environ["OLLAMA_MODEL"] = "llama3.2:3b"  # restore

    def test_get_provider_name_includes_model(self):
        from app.providers.ollama import OllamaProvider
        provider = OllamaProvider()
        assert "Ollama" in provider.get_provider_name()
        assert "llama" in provider.get_provider_name()


class TestProvidersWithoutKeys:
    """
    Tests that providers requiring API keys fail gracefully
    when keys are not present — no crashes, clean ValueError.
    """

    def test_openrouter_raises_value_error_without_key(self):
        from app.providers.openrouter import OpenRouterProvider
        original = os.environ.pop("OPENROUTER_API_KEY", None)
        try:
            with pytest.raises(ValueError) as exc_info:
                OpenRouterProvider()
            assert "OPENROUTER_API_KEY" in str(exc_info.value)
        finally:
            if original:
                os.environ["OPENROUTER_API_KEY"] = original

    def test_openai_raises_value_error_without_key(self):
        from app.providers.openai_provider import OpenAIProvider
        original = os.environ.pop("OPENAI_API_KEY", None)
        try:
            with pytest.raises(ValueError) as exc_info:
                OpenAIProvider()
            assert "OPENAI_API_KEY" in str(exc_info.value)
        finally:
            if original:
                os.environ["OPENAI_API_KEY"] = original

    def test_gemini_raises_value_error_without_key(self):
        from app.providers.gemini import GeminiProvider
        original = os.environ.pop("GEMINI_API_KEY", None)
        try:
            with pytest.raises(ValueError) as exc_info:
                GeminiProvider()
            assert "GEMINI_API_KEY" in str(exc_info.value)
        finally:
            if original:
                os.environ["GEMINI_API_KEY"] = original

    def test_claude_raises_value_error_without_key(self):
        from app.providers.claude import ClaudeProvider
        original = os.environ.pop("CLAUDE_API_KEY", None)
        try:
            with pytest.raises(ValueError) as exc_info:
                ClaudeProvider()
            assert "CLAUDE_API_KEY" in str(exc_info.value)
        finally:
            if original:
                os.environ["CLAUDE_API_KEY"] = original