from app.llm.mock_adapter import MockAdapter
from app.extractors.native_text import extract_native_text


pdf_path = "data/input/01_native_bank_statement.pdf"

text = extract_native_text(pdf_path)

adapter = MockAdapter()

result = adapter.extract(text)

print("=" * 60)
print("LLM RESULT")
print("=" * 60)

print(result)
