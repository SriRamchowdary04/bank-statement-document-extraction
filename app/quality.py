from datetime import datetime


def validate_transaction_quality(
    transaction: dict
) -> list[str]:

    errors = []

    # -----------------------------------------
    # Date
    # -----------------------------------------

    date_value = transaction.get("date")

    if not date_value:

        errors.append(
            "Transaction date is missing."
        )

    else:

        try:

            datetime.strptime(
                date_value,
                "%Y-%m-%d"
            )

        except ValueError:

            errors.append(
                f"Invalid date format: {date_value}"
            )

    # -----------------------------------------
    # Description
    # -----------------------------------------

    description = transaction.get(
        "description"
    )

    if not description or not str(
        description
    ).strip():

        errors.append(
            "Transaction description is missing."
        )

    # -----------------------------------------
    # Amount
    # -----------------------------------------

    amount = transaction.get(
        "amount"
    )

    if not isinstance(
        amount,
        (int, float)
    ):

        errors.append(
            "Transaction amount must be numeric."
        )

    # -----------------------------------------
    # Running balance
    # -----------------------------------------

    balance = transaction.get(
        "running_balance"
    )

    if not isinstance(
        balance,
        (int, float)
    ):

        errors.append(
            "Running balance must be numeric."
        )

    return errors


def validate_result_quality(
    result: dict
) -> list[str]:

    errors = []

    transactions = result.get(
        "transactions",
        []
    )

    document_status = result.get(
        "document_status"
    )

    # -----------------------------------------
    # Extracted document must have transactions
    # -----------------------------------------

    if (
        document_status == "extracted"
        and not transactions
    ):

        errors.append(
            "Document marked extracted "
            "but contains no transactions."
        )

        return errors

    # -----------------------------------------
    # Validate individual transactions
    # -----------------------------------------

    for index, transaction in enumerate(
        transactions,
        start=1
    ):

        transaction_errors = (
            validate_transaction_quality(
                transaction
            )
        )

        for error in transaction_errors:

            errors.append(
                f"Transaction {index}: {error}"
            )

    # -----------------------------------------
    # Running balance consistency
    # -----------------------------------------

    for index in range(
        1,
        len(transactions)
    ):

        previous = transactions[
            index - 1
        ]

        current = transactions[index]

        previous_balance = previous.get(
            "running_balance"
        )

        amount = current.get(
            "amount"
        )

        current_balance = current.get(
            "running_balance"
        )

        if not all(
            isinstance(value, (int, float))
            for value in [
                previous_balance,
                amount,
                current_balance
            ]
        ):

            continue

        expected_balance = (
            previous_balance + amount
        )

        if abs(
            expected_balance
            - current_balance
        ) > 0.01:

            errors.append(
                f"Transaction {index + 1}: "
                f"Running balance inconsistency. "
                f"Expected approximately "
                f"{expected_balance:.2f}, "
                f"got {current_balance:.2f}."
            )

    return errors
