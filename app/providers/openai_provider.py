import os
from openai import OpenAI
from app.providers.base import BaseProvider


class OpenAIProvider(BaseProvider):
    """
    Official OpenAI API provider.
    Uses the OpenAI SDK directly with your own API key.

    Requires OPENAI_API_KEY in environment.
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Add it to your .env file."
            )

        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def get_provider_name(self) -> str:
        return f"OpenAI ({self.model})"