import os
from app.providers.base import BaseProvider


# Valid provider names(used for validation)
SUPPORTED_PROVIDERS = ["ollama", "openrouter", "openai", "gemini", "claude"]


def get_provider() -> BaseProvider:
    """
    Factory function — reads AI_PROVIDER from environment
    and returns the correct provider instance.

    This is the only function the application calls.
    It shields everything else from knowing which provider is active.

    Returns:
        A provider instance that implements BaseProvider

    Raises:
        ValueError: if AI_PROVIDER is not set or not recognized
    """

    # Importing inside function to avoid circular imports
    # and to only load the SDK that's actually needed
    from app.providers.ollama import OllamaProvider
    from app.providers.openrouter import OpenRouterProvider
    from app.providers.openai_provider import OpenAIProvider
    from app.providers.gemini import GeminiProvider
    from app.providers.claude import ClaudeProvider

    provider_name = os.getenv("AI_PROVIDER", "ollama").lower().strip()

    providers = {
        "ollama":      OllamaProvider,
        "openrouter":  OpenRouterProvider,
        "openai":      OpenAIProvider,
        "gemini":      GeminiProvider,
        "claude":      ClaudeProvider,
    }

    if provider_name not in providers:
        raise ValueError(
            f"Unknown AI provider: '{provider_name}'. "
            f"Supported providers: {', '.join(SUPPORTED_PROVIDERS)}"
        )

    # Instantiate and return the correct provider
    return providers[provider_name]()