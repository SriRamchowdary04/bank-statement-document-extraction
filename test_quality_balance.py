from app.quality import validate_result_quality


result = {
    "document_status": "extracted",

    "transactions": [
        {
            "date": "2026-02-01",
            "description": "Deposit Salary",
            "amount": 3200.0,
            "running_balance": 420000.0
        },

        {
            "date": "2026-02-03",
            "description": "Utility Bill",
            "amount": -120.0,
            "running_balance": 4080.0
        }
    ]
}


errors = validate_result_quality(result)


print("=" * 60)
print("BALANCE QUALITY TEST")
print("=" * 60)


if errors:

    print("QUALITY CHECK FAILED:")

    for error in errors:
        print("-", error)

else:

    print(
        "QUALITY CHECK PASSED"
    )
