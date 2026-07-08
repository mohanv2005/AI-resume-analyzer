import os
from openai import OpenAI
from app.providers.base import BaseProvider


class OllamaProvider(BaseProvider):
    """
    Local LLM provider using Ollama.
    Ollama exposes an OpenAI-compatible API at localhost,
    so we reuse the OpenAI client pointed at a different base_url.

    No API key needed — Ollama runs entirely on your machine.
    """

    def __init__(self):
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

        # api_key="ollama" is a required placeholder — Ollama ignores it
        # but the OpenAI client requires a non-empty string
        self.client = OpenAI(
            base_url=base_url,
            api_key="ollama"
        )

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def get_provider_name(self) -> str:
        return f"Ollama ({self.model})"