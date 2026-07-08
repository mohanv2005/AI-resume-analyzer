import os
from google import genai
from app.providers.base import BaseProvider


class GeminiProvider(BaseProvider):
    """
    Google Gemini provider using the native google-genai SDK.
    Uses a different SDK than the OpenAI-compatible providers,
    but the generate() interface remains identical.

    Requires GEMINI_API_KEY in environment.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. "
                "Add it to your .env file."
            )

        self.model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")
        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text.strip()

    def get_provider_name(self) -> str:
        return f"Gemini ({self.model})"