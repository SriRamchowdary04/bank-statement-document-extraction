import json
import requests

from .base import LLMAdapter
from app.prompts import SYSTEM_PROMPT, build_user_prompt


class OllamaAdapter(LLMAdapter):

    name = "ollama"

    def __init__(self, model: str = "llama3.2:3b"):
        self.model = model
        self.name = model.replace(":", "_").replace(".", "_")

    def extract(self, document_text: str) -> dict:

        response = requests.post(
            "http://127.0.0.1:11434/api/chat",

            json={
                "model": self.model,
                "stream": False,
                "format": "json",

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
                ]
            },

            timeout=120
        )

        if not response.ok:

            print("OLLAMA API ERROR")
            print("MODEL:", self.model)
            print("STATUS CODE:", response.status_code)
            print("API RESPONSE:", response.text)

            response.raise_for_status()

        content = response.json()["message"]["content"]

        return json.loads(content)
