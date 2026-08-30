from app.llm.openai_adapter import OpenAIAdapter

adapter = OpenAIAdapter()

text = """
ABC BANK - BANK STATEMENT

2026-01-02 Salary Credit 2500.00 3500.00
2026-01-04 Rent Payment -900.00 2600.00
2026-01-06 ATM Withdrawal -100.00 2500.00
"""

result = adapter.extract(text)

print("=" * 60)
print("OPENAI RESULT")
print("=" * 60)

print(result)
