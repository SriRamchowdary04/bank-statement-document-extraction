import json
import requests

from .base import LLMAdapter
from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.prompts import SYSTEM_PROMPT, build_user_prompt


class GeminiAdapter(LLMAdapter):

    name = "gemini"

    def extract(self, document_text: str) -> dict:

        if not GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured"
            )

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{GEMINI_MODEL}:generateContent"
            f"?key={GEMINI_API_KEY}"
        )

        prompt = (
            SYSTEM_PROMPT
            + "\n\n"
            + build_user_prompt(document_text)
        )

        response = requests.post(
            url,

            headers={
                "Content-Type": "application/json"
            },

            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ],

                "generationConfig": {
                    "temperature": 0,
                    "responseMimeType": "application/json"
                }
            },

            timeout=120,
        )

        if not response.ok:

            print("\n" + "=" * 60)
            print("GEMINI API ERROR")
            print("=" * 60)
            print("STATUS CODE:", response.status_code)
            print("API RESPONSE:", response.text)
            print("=" * 60 + "\n")

        response.raise_for_status()

        response_data = response.json()

        model_output = (
            response_data["candidates"][0]
            ["content"]["parts"][0]["text"]
        )

        return json.loads(model_output)
