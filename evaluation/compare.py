from pathlib import Path
import json
from collections import defaultdict


OUTPUT_DIR = Path("data/output")


def load_results():

    results = []

    for path in sorted(
        OUTPUT_DIR.glob("*.json")
    ):

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        results.append(data)

    return results


def compare_models(results):

    comparison = defaultdict(
        lambda: {
            "files": 0,
            "successful": 0,
            "failed": 0,
            "quality_failures": 0,
            "transactions": 0,
            "total_amount": 0.0
        }
    )

    for result in results:

        model = result.get(
            "model",
            "unknown"
        )

        stats = comparison[model]

        stats["files"] += 1

        if result.get(
            "document_status"
        ) == "extracted":

            stats["successful"] += 1

        else:

            stats["failed"] += 1

        reason = (
            result.get("reason")
            or ""
        )

        if (
            "Quality validation failed"
            in reason
        ):

            stats["quality_failures"] += 1

        transactions = result.get(
            "transactions",
            []
        )

        stats["transactions"] += len(
            transactions
        )

        for transaction in transactions:

            amount = transaction.get(
                "amount"
            )

            if isinstance(
                amount,
                (int, float)
            ):

                stats["total_amount"] += amount

    return dict(comparison)


def main():

    results = load_results()

    comparison = compare_models(
        results
    )

    print("=" * 70)
    print("LLM MODEL COMPARISON")
    print("=" * 70)

    for model, stats in (
        comparison.items()
    ):

        print("\nMODEL:", model)

        print(
            "Output files:",
            stats["files"]
        )

        print(
            "Successful:",
            stats["successful"]
        )

        print(
            "Failed:",
            stats["failed"]
        )

        print(
            "Quality failures:",
            stats["quality_failures"]
        )

        print(
            "Transactions:",
            stats["transactions"]
        )

        print(
            "Total transaction amount:",
            round(
                stats["total_amount"],
                2
            )
        )


if __name__ == "__main__":
    main()
