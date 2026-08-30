from pathlib import Path
import json
from collections import defaultdict


OUTPUT_DIR = Path("data/output")
REPORT_PATH = Path("evaluation/evaluation_report.json")


def load_results():

    results = []

    for path in sorted(OUTPUT_DIR.glob("*.json")):

        try:

            data = json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )

            data["_file"] = path.name

            results.append(data)

        except Exception as exc:

            results.append(
                {
                    "_file": path.name,
                    "document_status":
                        "could_not_process",
                    "reason":
                        f"Could not read JSON: {exc}",
                    "transactions": []
                }
            )

    return results


def get_original_document(filename):

    name = filename

    # Remove statement suffix
    if "_statement_" in name:

        name = name.split(
            "_statement_"
        )[0]

    # Remove model suffix
    if "__" in name:

        name = name.split(
            "__"
        )[0]

    return name


def build_report(results):

    input_documents = sorted(
        {
            get_original_document(
                result["_file"]
            )
            for result in results
        }
    )

    total_input_documents = len(
        input_documents
    )

    total_output_files = len(
        results
    )

    successful = sum(
        1
        for result in results
        if result.get("document_status")
        == "extracted"
    )

    failed = sum(
        1
        for result in results
        if result.get("document_status")
        == "could_not_process"
    )

    total_transactions = sum(
        len(
            result.get(
                "transactions",
                []
            )
        )
        for result in results
    )

    quality_failures = sum(
        1
        for result in results
        if "Quality validation failed"
        in (result.get("reason") or "")
    )

    ocr_review_required = sum(
        1
        for result in results
        if "OCR confidence too low"
        in (result.get("reason") or "")
    )

    password_protected = sum(
        1
        for result in results
        if "Password-protected PDF"
        in (result.get("reason") or "")
    )

    not_bank_statement = sum(
        1
        for result in results
        if "does not appear to be a bank statement"
        in (result.get("reason") or "")
    )

    by_model = defaultdict(
        lambda: {
            "output_files": 0,
            "successful": 0,
            "failed": 0,
            "transactions": 0,
            "quality_failures": 0
        }
    )

    for result in results:

        model = result.get(
            "model",
            "unknown"
        )

        stats = by_model[model]

        stats["output_files"] += 1

        if result.get(
            "document_status"
        ) == "extracted":

            stats["successful"] += 1

        else:

            stats["failed"] += 1

        stats["transactions"] += len(
            result.get(
                "transactions",
                []
            )
        )

        if "Quality validation failed" in (result.get("reason") or ""):

            stats["quality_failures"] += 1

    return {

        "summary": {

            "input_documents":
                total_input_documents,

            "output_files":
                total_output_files,

            "successful_extractions":
                successful,

            "failed_extractions":
                failed,

            "quality_failures":
                quality_failures,

            "ocr_review_required":
                ocr_review_required,

            "password_protected":
                password_protected,

            "not_bank_statements":
                not_bank_statement,

            "total_transactions":
                total_transactions
        },

        "by_model":
            dict(by_model),

        "results":
            results
    }


def main():

    results = load_results()

    report = build_report(
        results
    )

    REPORT_PATH.write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print("=" * 70)
    print("DOCUMENT EXTRACTION EVALUATION")
    print("=" * 70)

    summary = report[
        "summary"
    ]

    print(
        "Input documents:",
        summary[
            "input_documents"
        ]
    )

    print(
        "Output files:",
        summary[
            "output_files"
        ]
    )

    print(
        "Successful extractions:",
        summary[
            "successful_extractions"
        ]
    )

    print(
        "Failed extractions:",
        summary[
            "failed_extractions"
        ]
    )

    print(
        "Quality failures:",
        summary[
            "quality_failures"
        ]
    )

    print(
        "OCR review required:",
        summary[
            "ocr_review_required"
        ]
    )

    print(
        "Password protected:",
        summary[
            "password_protected"
        ]
    )

    print(
        "Not bank statements:",
        summary[
            "not_bank_statements"
        ]
    )

    print(
        "Total transactions:",
        summary[
            "total_transactions"
        ]
    )

    print("\nBy model:")

    for model, stats in (
        report["by_model"].items()
    ):

        print(
            f"  {model}: "
            f"{stats['successful']} successful, "
            f"{stats['failed']} failed, "
            f"{stats['quality_failures']} quality failures, "
            f"{stats['transactions']} transactions"
        )

    print(
        "\nReport:",
        REPORT_PATH
    )


if __name__ == "__main__":
    main()
