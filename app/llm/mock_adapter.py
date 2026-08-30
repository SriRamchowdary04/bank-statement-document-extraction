import re

from .base import LLMAdapter


class MockAdapter(LLMAdapter):

    name = "mock"

    def extract(
        self,
        document_text: str
    ) -> dict:

        transactions = []

        lines = document_text.splitlines()

        for line in lines:

            match = re.search(
                r"(\d{4}-\d{2}-\d{2})\s+"
                r"(.+?)\s+"
                r"(-?\d+(?:\.\d{2})?)\s+"
                r"(-?\d+(?:\.\d{2})?)$",
                line.strip()
            )

            if not match:
                continue

            date = match.group(1)
            description = match.group(2).strip()
            amount = float(match.group(3))
            balance = float(match.group(4))

            transactions.append(
                {
                    "date": date,
                    "description": description,
                    "amount": amount,
                    "running_balance": balance,
                }
            )

        if not transactions:

            return {
                "document_status":
                    "could_not_process",

                "reason":
                    "Mock extractor could not identify transactions.",

                "transactions": [],
            }

        return {
            "document_status":
                "extracted",

            "reason":
                None,

            "transactions":
                transactions,
        }
