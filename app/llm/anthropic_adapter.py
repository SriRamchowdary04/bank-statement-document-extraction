import json
import requests

from .base import LLMAdapter
from app.config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL
from app.prompts import SYSTEM_PROMPT, build_user_prompt


class AnthropicAdapter(LLMAdapter):

    name = "anthropic"

    def extract(self, document_text: str) -> dict:

        if not ANTHROPIC_API_KEY:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not configured"
            )

        response = requests.post(
            "https://api.anthropic.com/v1/messages",

            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },

            json={
                "model": ANTHROPIC_MODEL,
                "max_tokens": 4096,
                "system": SYSTEM_PROMPT,
                "messages": [
                    {
                        "role": "user",
                        "content": build_user_prompt(
                            document_text
                        )
                    }
                ],
            },

            timeout=120,
        )

        if not response.ok:

            print("\n" + "=" * 60)
            print("ANTHROPIC API ERROR")
            print("=" * 60)
            print("STATUS CODE:", response.status_code)
            print("API RESPONSE:", response.text)
            print("=" * 60 + "\n")

        response.raise_for_status()

        response_data = response.json()

        model_output = response_data["content"][0]["text"]

        return json.loads(model_output)
