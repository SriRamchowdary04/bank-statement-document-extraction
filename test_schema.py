from app.schemas import ExtractionResult


good_result = {
    "detected_format": "native_text",
    "model": "mock",
    "document_status": "extracted",
    "reason": None,
    "transactions": [
        {
            "date": "2026-03-01",
            "description": "Deposit",
            "amount": 1000.00,
            "running_balance": 1800.00
        }
    ]
}


print("=" * 60)
print("VALID JSON TEST")
print("=" * 60)

validated = ExtractionResult.model_validate(good_result)

print(validated.model_dump())


bad_result = {
    "detected_format": "native_text",
    "model": "mock",
    "document_status": "extracted",
    "reason": None,
    "transactions": [
        {
            "date": "wrong-date",
            "description": "Deposit"
        }
    ]
}


print("\n")
print("=" * 60)
print("INVALID JSON TEST")
print("=" * 60)

try:

    ExtractionResult.model_validate(bad_result)

except Exception as exc:

    print("Validation correctly failed:")
    print(exc)
