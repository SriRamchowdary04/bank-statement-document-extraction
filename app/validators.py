import re


BANK_TERMS = [
    "bank",
    "statement",
    "account",
    "transaction",
    "balance",
    "debit",
    "credit",
    "withdrawal",
    "deposit",
]


def looks_like_bank_statement(text: str) -> bool:

    lower = text.lower()

    # -----------------------------------------
    # Normal keyword matching
    # -----------------------------------------

    score = sum(
        1
        for term in BANK_TERMS
        if term in lower
    )

    # -----------------------------------------
    # Date detection
    # -----------------------------------------

    has_date = bool(
        re.search(
            r"\b\d{4}[-/]\d{2}[-/]\d{2}\b",
            text
        )
    )

    # OCR can damage dates, so also look for
    # date-like sequences.
    has_date_like = bool(
        re.search(
            r"\b\d{6,8}\b",
            text
        )
    )

    # -----------------------------------------
    # Money detection
    # -----------------------------------------

    has_money = bool(
        re.search(
            r"[$₹€£]?\s*\d[\d,]*\.\d{2}",
            text
        )
    )

    # OCR may remove decimal points.
    has_money_like = bool(
        re.search(
            r"\b\d{3,7}\b",
            text
        )
    )

    # -----------------------------------------
    # Transaction-line detection
    # -----------------------------------------

    lines = text.splitlines()

    transaction_like_lines = 0

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if (
            re.search(r"\d{6,8}", line)
            and re.search(r"\d{3,7}", line)
        ):
            transaction_like_lines += 1

    # -----------------------------------------
    # Strong native-text case
    # -----------------------------------------

    if score >= 2 and (
        has_date or has_money
    ):
        return True

    # -----------------------------------------
    # OCR / scanned document case
    # -----------------------------------------

    if transaction_like_lines >= 2 and (
        has_date_like or has_money_like
    ):
        return True

    # -----------------------------------------
    # OCR may still retain one bank keyword
    # plus transaction patterns.
    # -----------------------------------------

    if score >= 1 and transaction_like_lines >= 2:
        return True

    return False


def split_merged_statements(text: str) -> list[str]:

    header_pattern = re.compile(
        r"(?im)(?=^.*BANK\s+STATEMENT\b)"
    )

    matches = list(
        header_pattern.finditer(text)
    )

    if len(matches) <= 1:
        return [text.strip()]

    statements = []

    for index, match in enumerate(matches):

        start = match.start()

        if index + 1 < len(matches):

            end = matches[
                index + 1
            ].start()

        else:

            end = len(text)

        statement = text[
            start:end
        ].strip()

        if statement:
            statements.append(
                statement
            )

    return statements
