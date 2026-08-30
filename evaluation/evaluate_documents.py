from pathlib import Path
import json


TEST_CASES = Path(
    "evaluation/test_cases.json"
)

OUTPUT_DIR = Path(
    "data/output"
)


def load_json(path):

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def get_output_files(document):

    return sorted(
        OUTPUT_DIR.glob(
            f"{document.replace('.pdf', '')}*.json"
        )
    )


def evaluate_case(
    document,
    expected
):

    files = get_output_files(
        document
    )

    if not files:

        return {
            "document": document,
            "status": "FAIL",
            "reason": "No output file found."
        }

    results = [
        load_json(path)
        for path in files
    ]

    expected_result = expected[
        "expected_result"
    ]

    # ------------------------------------------------
    # Password protected
    # ------------------------------------------------

    if expected_result == "could_not_process":

        reasons = [
            result.get("reason") or ""
            for result in results
        ]

        if (
            expected["expected_route"]
            == "password_protected"
        ):

            passed = any(
                "Password-protected PDF"
                in reason
                for reason in reasons
            )

        else:

            passed = any(
                "does not appear to be a bank statement"
                in reason
                for reason in reasons
            )

        return {
            "document": document,
            "status":
                "PASS" if passed else "FAIL",
            "expected":
                expected_result,
            "actual":
                "could_not_process"
                if passed
                else "unexpected",
            "output_files":
                len(files)
        }

    # ------------------------------------------------
    # Expected quality review
    # ------------------------------------------------

    if expected_result == "quality_review":

        quality_failure = any(
            "Quality validation failed"
            in (result.get("reason") or "")
            for result in results
        )

        return {
            "document": document,
            "status":
                "PASS"
                if quality_failure
                else "REVIEW",
            "expected":
                expected_result,
            "actual":
                "quality_failure"
                if quality_failure
                else "extracted",
            "output_files":
                len(files)
        }

    # ------------------------------------------------
    # Expected successful extraction
    # ------------------------------------------------

    if expected_result == "extracted":

        extracted = all(
            result.get(
                "document_status"
            ) == "extracted"
            for result in results
        )

        result = {
            "document": document,
            "status":
                "PASS"
                if extracted
                else "FAIL",
            "expected":
                expected_result,
            "actual":
                "extracted"
                if extracted
                else "failed",
            "output_files":
                len(files)
        }

        # --------------------------------------------
        # Merged statement check
        # --------------------------------------------

        if "expected_statements" in expected:

            expected_count = expected[
                "expected_statements"
            ]

            actual_count = len(files)

            result[
                "expected_statements"
            ] = expected_count

            result[
                "actual_statements"
            ] = actual_count

            if actual_count != expected_count:

                result["status"] = "FAIL"

        return result

    return {
        "document": document,
        "status": "FAIL",
        "reason": "Unknown expected result."
    }


def main():

    test_cases = load_json(
        TEST_CASES
    )

    results = []

    print("=" * 70)
    print("DOCUMENT-LEVEL EVALUATION")
    print("=" * 70)

    for document, expected in (
        test_cases.items()
    ):

        result = evaluate_case(
            document,
            expected
        )

        results.append(result)

        print(
            f"\n{result['status']:6} "
            f"{document}"
        )

        if "reason" in result:

            print(
                "       ",
                result["reason"]
            )

        if "expected_statements" in result:

            print(
                "        Statements:",
                result["actual_statements"],
                "/",
                result["expected_statements"]
            )

    passed = sum(
        1
        for result in results
        if result["status"] == "PASS"
    )

    total = len(results)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(
        "Passed:",
        passed,
        "/",
        total
    )

    print(
        "Document handling accuracy:",
        f"{passed / total * 100:.2f}%"
        if total
        else "0%"
    )


if __name__ == "__main__":
    main()
