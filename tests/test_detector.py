from pathlib import Path
from reportlab.pdfgen import canvas
from app.detector import inspect_pdf

def test_native_text_detection(tmp_path):
    p = tmp_path / "native.pdf"
    c = canvas.Canvas(str(p))
    c.drawString(50, 750, "Bank Statement Account Transaction Balance")
    c.drawString(50, 730, "2026-01-01 Deposit 100.00 1100.00")
    c.save()

    result = inspect_pdf(str(p))
    assert result["detected_format"] == "native_text"
