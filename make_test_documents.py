from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from pypdf import PdfReader, PdfWriter
import io, shutil

OUT = Path("data/input")
OUT.mkdir(parents=True, exist_ok=True)

def native_pdf(path):
    c = canvas.Canvas(str(path), pagesize=A4)
    c.setFont("Helvetica", 11)
    rows = [
        ("2026-01-02", "Salary Credit", "2500.00", "3500.00"),
        ("2026-01-04", "Rent Payment", "-900.00", "2600.00"),
        ("2026-01-06", "ATM Withdrawal", "-100.00", "2500.00"),
        ("2026-01-08", "Grocery Store", "-80.50", "2419.50"),
    ]
    c.drawString(50, 800, "ABC BANK - BANK STATEMENT")
    c.drawString(50, 780, "Account Statement | Account: XXXX1234")
    y = 740
    for date, desc, amount, bal in rows:
        c.drawString(50, y, f"{date}   {desc:<25} {amount:>10}   {bal:>10}")
        y -= 22
    c.save()

def statement_image():
    img = Image.new("RGB", (1700, 2200), "white")
    d = ImageDraw.Draw(img)
    d.text((100, 100), "ABC BANK - BANK STATEMENT", fill="black")
    d.text((100, 160), "Account: XXXX5678", fill="black")
    y = 260
    rows = [
        "2026-02-01  Deposit Salary          3200.00   4200.00",
        "2026-02-03  Utility Bill             -120.00   4080.00",
        "2026-02-05  Restaurant                -55.00   4025.00",
        "2026-02-07  Transfer                  -500.00   3525.00",
    ]
    for row in rows:
        d.text((100, y), row, fill="black")
        y += 70
    return img

def image_only_pdf(path):
    img = statement_image()
    c = canvas.Canvas(str(path), pagesize=A4)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    c.drawImage(ImageReader(buf), 0, 0, width=A4[0], height=A4[1])
    c.save()

def scanned_pdf(path):
    img = statement_image().convert("L")
    c = canvas.Canvas(str(path), pagesize=A4)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    c.drawImage(ImageReader(buf), 0, 0, width=A4[0], height=A4[1])
    c.save()

def photocopy_pdf(path):
    img = statement_image().convert("L")
    img = ImageEnhance.Contrast(img).enhance(0.55)
    img = img.filter(ImageFilter.GaussianBlur(0.8))
    img = img.rotate(1.0, expand=True, fillcolor="white")
    c = canvas.Canvas(str(path), pagesize=A4)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    c.drawImage(ImageReader(buf), 0, 0, width=A4[0], height=A4[1])
    c.save()

def merged_pdf(path):
    c = canvas.Canvas(str(path), pagesize=A4)
    for account, first in [("XXXX1111", "1800.00"), ("XXXX2222", "950.00")]:
        c.drawString(50, 800, "ABC BANK - BANK STATEMENT")
        c.drawString(50, 780, f"Statement Period | Account: {account}")
        c.drawString(50, 740, f"2026-03-01 Deposit 1000.00 {first}")
        c.drawString(50, 718, f"2026-03-03 Purchase -100.00 {float(first)-100:.2f}")
        c.showPage()
    c.save()

def password_pdf(path):
    plain = OUT / "_plain_password.pdf"
    native_pdf(plain)
    reader = PdfReader(str(plain))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt("demo-password")
    with open(path, "wb") as f:
        writer.write(f)
    plain.unlink(missing_ok=True)

def non_bank_pdf(path):
    c = canvas.Canvas(str(path), pagesize=A4)
    c.drawString(50, 800, "EMPLOYEE HANDBOOK")
    c.drawString(50, 770, "This document contains company policies and procedures.")
    c.save()

native_pdf(OUT / "01_native_bank_statement.pdf")
image_only_pdf(OUT / "02_image_only_statement.pdf")
scanned_pdf(OUT / "03_scanned_statement.pdf")
photocopy_pdf(OUT / "04_photocopy_statement.pdf")
merged_pdf(OUT / "05_merged_statements.pdf")
password_pdf(OUT / "06_password_protected.pdf")
non_bank_pdf(OUT / "07_not_a_bank_statement.pdf")

print("Created 7 synthetic test PDFs in data/input/")
