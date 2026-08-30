import pytesseract

from PIL import ImageOps, ImageEnhance
from pypdfium2 import PdfDocument


OCR_CONFIDENCE_THRESHOLD = 60.0


def preprocess_image(image):

    image = ImageOps.grayscale(image)

    enhancer = ImageEnhance.Contrast(image)

    image = enhancer.enhance(2.0)

    image = image.point(
        lambda pixel:
        0 if pixel < 180 else 255
    )

    return image


def extract_ocr_text(path: str):

    pdf = PdfDocument(path)

    chunks = []

    page_confidences = []

    for index in range(len(pdf)):

        page = pdf[index]

        bitmap = page.render(
            scale=3.0
        )

        image = bitmap.to_pil()

        image = preprocess_image(
            image
        )

        # -----------------------------------------
        # Extract text
        # -----------------------------------------

        text = pytesseract.image_to_string(
            image,
            config="--psm 6"
        )

        chunks.append(
            f"\n--- PAGE {index + 1} ---\n{text}"
        )

        # -----------------------------------------
        # Calculate OCR confidence
        # -----------------------------------------

        data = pytesseract.image_to_data(
            image,
            config="--psm 6",
            output_type=pytesseract.Output.DICT
        )

        confidences = []

        for confidence in data["conf"]:

            try:

                value = float(
                    confidence
                )

                if value >= 0:
                    confidences.append(
                        value
                    )

            except ValueError:

                continue

        if confidences:

            page_confidence = (
                sum(confidences)
                / len(confidences)
            )

        else:

            page_confidence = 0.0

        page_confidences.append(
            page_confidence
        )

    # -----------------------------------------
    # Overall document confidence
    # -----------------------------------------

    if page_confidences:

        average_confidence = (
            sum(page_confidences)
            / len(page_confidences)
        )

    else:

        average_confidence = 0.0

    return {
        "text": "\n".join(chunks).strip(),
        "ocr_confidence": round(
            average_confidence,
            2
        ),
        "needs_review":
            average_confidence
            < OCR_CONFIDENCE_THRESHOLD
    }
