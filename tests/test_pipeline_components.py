from pathlib import Path

import pytest

from app.extractors.native_text import extract_native_text
from app.schemas import ExtractionResult
from app.validators import looks_like_bank_statement
from app.quality import validate_result_quality


BASE = Path("data/input")


def test_native_extraction():

    pdf = BASE / "01_native_bank_statement.pdf"

    text = extract_native_text(str(pdf))

    assert text
    assert "ABC BANK" in text
    assert "Salary Credit" in text


def test_bank_statement_validator():

    text = """
    ABC BANK - BANK STATEMENT
    Account: XXXX1111

    2026-01-02 Salary Credit 2500.00 3500.00
    """

    assert looks_like_bank_statement(text) is True


def test_schema_valid_transaction():

    result = ExtractionResult(
        detected_format="native_text",
        model="mock",
        document_status="extracted",
        reason=None,
        transactions=[
            {
                "date": "2026-01-02",
                "description": "Salary Credit",
                "amount": 2500.0,
                "running_balance": 3500.0
            }
        ]
    )

    assert len(result.transactions) == 1
    assert result.transactions[0].amount == 2500.0


def test_schema_rejects_missing_amount():

    with pytest.raises(Exception):

        ExtractionResult(
            detected_format="native_text",
            model="mock",
            document_status="extracted",
            reason=None,
            transactions=[
                {
                    "date": "2026-01-02",
                    "description": "Salary Credit",
                    "running_balance": 3500.0
                }
            ]
        )


def test_quality_detects_bad_balance():

    result = {
        "document_status": "extracted",

        "transactions": [
            {
                "date": "2026-01-02",
                "description": "Deposit",
                "amount": 1000.0,
                "running_balance": 5000.0
            },
            {
                "date": "2026-01-03",
                "description": "Purchase",
                "amount": -100.0,
                "running_balance": 2000.0
            }
        ]
    }

    errors = validate_result_quality(result)

    assert errors

    assert any(
        "Running balance inconsistency"
        in error
        for error in errors
    )
