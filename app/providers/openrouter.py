import os
from openai import OpenAI
from app.providers.base import BaseProvider


class OpenRouterProvider(BaseProvider):
    """
    Cloud AI gateway using OpenRouter.
    OpenRouter provides access to many models (Llama, Gemini, Claude, GPT)
    through a single OpenAI-compatible API endpoint.

    Requires OPENROUTER_API_KEY in environment.
    """

    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found in environment variables. "
                "Add it to your .env file."
            )

        self.model = os.getenv(
            "OPENROUTER_MODEL",
            "meta-llama/llama-3.2-3b-instruct:free"
        )

        # OpenRouter is OpenAI-compatible — same client, different base_url
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def get_provider_name(self) -> str:
        return f"OpenRouter ({self.model})"