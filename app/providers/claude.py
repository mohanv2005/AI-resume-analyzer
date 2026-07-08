import os
import anthropic
from app.providers.base import BaseProvider


class ClaudeProvider(BaseProvider):
    """
    Anthropic Claude provider using the native anthropic SDK.
    Claude uses a messages API similar to OpenAI but with
    slightly different parameters (max_tokens is required).

    Requires CLAUDE_API_KEY in environment.
    """

    def __init__(self):
        api_key = os.getenv("CLAUDE_API_KEY")
        if not api_key:
            raise ValueError(
                "CLAUDE_API_KEY not found in environment variables. "
                "Add it to your .env file."
            )

        self.model = os.getenv("CLAUDE_MODEL", "claude-3-haiku-20240307")
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate(self, prompt: str) -> str:
        # Claude requires max_tokens to be explicitly set
        # 2048 should be sufficient for resume analysis 
        message = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()

    def get_provider_name(self) -> str:
        return f"Claude ({self.model})"