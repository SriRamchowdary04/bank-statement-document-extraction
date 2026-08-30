from pathlib import Path

import pytesseract
from PIL import ImageOps, ImageEnhance
from pypdfium2 import PdfDocument


pdf_path = Path(
    "data/input/04_photocopy_statement.pdf"
)


pdf = PdfDocument(
    str(pdf_path)
)


for page_number in range(
    len(pdf)
):

    page = pdf[page_number]

    bitmap = page.render(
        scale=3.0
    )

    image = bitmap.to_pil()

    image = ImageOps.grayscale(
        image
    )

    image = ImageEnhance.Contrast(
        image
    ).enhance(2.0)

    image = image.point(
        lambda pixel:
        0 if pixel < 180 else 255
    )

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
            pass

    average_confidence = (
        sum(confidences)
        / len(confidences)
        if confidences
        else 0
    )

    print("=" * 60)
    print(
        f"PAGE {page_number + 1}"
    )
    print("=" * 60)

    print(
        "Words:",
        len(confidences)
    )

    print(
        "Average OCR confidence:",
        round(
            average_confidence,
            2
        )
    )
