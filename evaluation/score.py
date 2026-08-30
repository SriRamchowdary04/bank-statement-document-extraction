from pathlib import Path
import json


GROUND_TRUTH = Path(
    "evaluation/ground_truth.json"
)

OUTPUT_DIR = Path(
    "data/output"
)


def load_ground_truth():

    return json.loads(
        GROUND_TRUTH.read_text(
            encoding="utf-8"
        )
    )


def compare_value(
    expected,
    actual
):

    if isinstance(
        expected,
        (int, float)
    ) and isinstance(
        actual,
        (int, float)
    ):

        return abs(
            expected - actual
        ) < 0.01

    return expected == actual


def score_transactions(
    expected,
    actual
):

    fields = [
        "date",
        "description",
        "amount",
        "running_balance"
    ]

    total = 0
    correct = 0

    field_stats = {
        field: {
            "correct": 0,
            "total": 0
        }
        for field in fields
    }

    transaction_count = min(
        len(expected),
        len(actual)
    )

    for index in range(
        transaction_count
    ):

        expected_tx = expected[index]
        actual_tx = actual[index]

        for field in fields:

            field_stats[field][
                "total"
            ] += 1

            total += 1

            if compare_value(
                expected_tx.get(field),
                actual_tx.get(field)
            ):

                field_stats[field][
                    "correct"
                ] += 1

                correct += 1

    overall_accuracy = (
        correct / total * 100
        if total
        else 0
    )

    for field in fields:

        stats = field_stats[field]

        stats["accuracy"] = (
            stats["correct"]
            / stats["total"]
            * 100
            if stats["total"]
            else 0
        )

    return {
        "expected_transactions":
            len(expected),

        "actual_transactions":
            len(actual),

        "field_accuracy":
            field_stats,

        "overall_accuracy":
            round(
                overall_accuracy,
                2
            )
    }


def main():

    ground_truth = (
        load_ground_truth()
    )

    print("=" * 70)
    print("EXTRACTION ACCURACY REPORT")
    print("=" * 70)

    model_results = {}

    for output_file in sorted(
        OUTPUT_DIR.glob("*.json")
    ):

        filename = output_file.stem

        # Remove model suffix
        if "__" not in filename:
            continue

        document_key, model = (
            filename.rsplit(
                "__",
                1
            )
        )

        if document_key not in ground_truth:
            continue

        data = json.loads(
            output_file.read_text(
                encoding="utf-8"
            )
        )

        expected = ground_truth[
            document_key
        ]

        actual = data.get(
            "transactions",
            []
        )

        score = score_transactions(
            expected,
            actual
        )

        model_results.setdefault(
            model,
            []
        ).append(
            {
                "document":
                    document_key,

                "score":
                    score
            }
        )

    for model, results in (
        model_results.items()
    ):

        print("\n")
        print(
            "MODEL:",
            model
        )

        all_scores = []

        for result in results:

            score = result["score"]

            all_scores.append(
                score["overall_accuracy"]
            )

            print(
                "\nDocument:",
                result["document"]
            )

            print(
                "Expected transactions:",
                score[
                    "expected_transactions"
                ]
            )

            print(
                "Actual transactions:",
                score[
                    "actual_transactions"
                ]
            )

            print(
                "Overall accuracy:",
                f"{score['overall_accuracy']}%"
            )

            for field, stats in (
                score[
                    "field_accuracy"
                ].items()
            ):

                print(
                    f"  {field}: "
                    f"{stats['accuracy']:.2f}%"
                )

        if all_scores:

            average = (
                sum(all_scores)
                / len(all_scores)
            )

            print(
                "\nAverage model accuracy:",
                f"{average:.2f}%"
            )


if __name__ == "__main__":
    main()
