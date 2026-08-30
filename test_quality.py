from app.quality import validate_result_quality


good_result = {
    "document_status": "extracted",
    "transactions": [
        {
            "date": "2026-03-01",
            "description": "Deposit",
            "amount": 1000.00,
            "running_balance": 1800.00
        }
    ]
}


bad_result = {
    "document_status": "extracted",
    "transactions": [
        {
            "date": "wrong-date",
            "description": "",
            "amount": "one thousand",
            "running_balance": None
        }
    ]
}


print("=" * 60)
print("GOOD RESULT")
print("=" * 60)

print(
    validate_result_quality(
        good_result
    )
)


print("\n")
print("=" * 60)
print("BAD RESULT")
print("=" * 60)

errors = validate_result_quality(
    bad_result
)

for error in errors:

    print("-", error)
