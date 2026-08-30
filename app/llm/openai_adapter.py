import json
import requests

from .base import LLMAdapter
from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.prompts import SYSTEM_PROMPT, build_user_prompt


class OpenAIAdapter(LLMAdapter):

    name = "openai"

    def extract(self, document_text: str) -> dict:

        if not OPENAI_API_KEY:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured"
            )

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",

            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },

            json={
                "model": OPENAI_MODEL,
                "temperature": 0,

                "response_format": {
                    "type": "json_object"
                },

                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
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

        # Check for API errors
        if not response.ok:

            print("\n" + "=" * 60)
            print("OPENAI API ERROR")
            print("=" * 60)

            print(
                "STATUS CODE:",
                response.status_code
            )

            print(
                "API RESPONSE:",
                response.text
            )

            print("=" * 60 + "\n")

        # Raise the HTTP error if request failed
        response.raise_for_status()

        # Get JSON response from OpenAI
        response_data = response.json()

        # Get the model's actual message
        model_output = (
            response_data["choices"][0]
            ["message"]["content"]
        )

        # Convert JSON string to Python dictionary
        result = json.loads(model_output)

        return result