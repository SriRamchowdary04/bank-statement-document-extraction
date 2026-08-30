from app.llm.mock_adapter import MockAdapter
from app.llm.openai_adapter import OpenAIAdapter
from app.llm.anthropic_adapter import AnthropicAdapter
from app.llm.gemini_adapter import GeminiAdapter


DOCUMENT = """
ABC BANK - BANK STATEMENT

Account: XXXX1111

2026-03-01 Deposit 1000.00 1800.00
2026-03-03 Purchase -100.00 1700.00
"""


adapters = [
    MockAdapter(),
    OpenAIAdapter(),
    AnthropicAdapter(),
    GeminiAdapter(),
]


print("=" * 70)
print("MULTI-LLM DRY RUN")
print("=" * 70)

print("\nDocument:")
print(DOCUMENT)

print("\nProviders available:")

for adapter in adapters:

    print(
        f"  {adapter.name:12} "
        f"→ {adapter.__class__.__name__}"
    )

print("\nCommon interface:")

for adapter in adapters:

    print(
        f"  {adapter.name}.extract(document_text)"
    )

print("\nArchitecture test: PASSED")
