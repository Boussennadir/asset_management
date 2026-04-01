from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm
from pathlib import Path
import os


def get_barcode_directory():
    folder = Path.home() / "Documents" / "AssetApp" / "Barcodes"
    folder.mkdir(parents=True, exist_ok=True)
    return str(folder)


def generate_barcode_pdf(equipement):
    value = str(equipement.numero_serie)

    width = 70 * mm
    height = 35 * mm

    file_path = os.path.join(
        get_barcode_directory(),
        f"barcode_{value}.pdf"
    )

    c = canvas.Canvas(file_path, pagesize=(width, height))

    barcode = code128.Code128(
        value,
        barHeight=15 * mm,
        barWidth=0.5
    )

    barcode_width = barcode.width
    barcode_x = (width - barcode_width) / 2
    barcode_y = height / 2 - 5

    barcode.drawOn(c, barcode_x, barcode_y)

    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(width / 2, 10, value)

    c.setFont("Helvetica", 7)
    c.drawCentredString(width / 2, 3, equipement.nom)

    c.save()

    # 🔥 فتح الملف مباشرة
    os.startfile(file_path)

    return file_path