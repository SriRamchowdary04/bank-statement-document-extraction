from pypdf import PdfReader


def inspect_pdf(path: str) -> dict:
    """
    Inspect a PDF and determine whether it contains
    native/selectable text or is image-based.
    """

    reader = PdfReader(path)

    # --------------------------------------------------
    # 1. Check whether the PDF is password protected
    # --------------------------------------------------
    if reader.is_encrypted:
        return {
            "status": "password_protected",
            "detected_format": "image_based",
            "page_count": None,
            "text_chars": 0,
            "pages_with_text": 0,
        }

    # --------------------------------------------------
    # 2. Extract whatever text layer exists
    # --------------------------------------------------
    page_texts = []

    for page in reader.pages:
        try:
            text = page.extract_text() or ""
            page_texts.append(text)
        except Exception:
            page_texts.append("")

    # --------------------------------------------------
    # 3. Calculate how much usable text exists
    # --------------------------------------------------
    text_chars = sum(
        len(text.strip())
        for text in page_texts
    )

    pages_with_text = sum(
        bool(text.strip())
        for text in page_texts
    )

    # --------------------------------------------------
    # 4. Decide document type
    # --------------------------------------------------
    if text_chars >= 50 and pages_with_text > 0:
        detected_format = "native_text"
    else:
        detected_format = "image_based"

    # --------------------------------------------------
    # 5. Return detection information
    # --------------------------------------------------
    return {
        "status": "ok",
        "detected_format": detected_format,
        "page_count": len(reader.pages),
        "text_chars": text_chars,
        "pages_with_text": pages_with_text,
    }