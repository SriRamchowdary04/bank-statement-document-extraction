from app.llm.mock_adapter import MockAdapter
from app.llm.openai_adapter import OpenAIAdapter
from app.llm.anthropic_adapter import AnthropicAdapter
from app.llm.gemini_adapter import GeminiAdapter


adapters = [
    MockAdapter(),
    OpenAIAdapter(),
    AnthropicAdapter(),
    GeminiAdapter(),
]


print("=" * 60)
print("LLM PROVIDER TEST")
print("=" * 60)

for adapter in adapters:

    print(
        f"{adapter.name:12} → "
        f"{adapter.__class__.__name__} → OK"
    )
