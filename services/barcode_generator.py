from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm
from pathlib import Path
import os


# 📁 نفس dossier
def get_barcode_directory():
    folder = Path.home() / "Documents" / "AssetApp" / "Barcodes"
    folder.mkdir(parents=True, exist_ok=True)
    return str(folder)


def generate_barcode_pdf(equipements):
    """
    equipements = list of objects (each has nom + numero_serie)
    """

    file_path = os.path.join(get_barcode_directory(), "barcodes.pdf")

    c = canvas.Canvas(file_path, pagesize=A4)

    x = 20
    y = 800

    for eq in equipements:

        value = str(eq.numero_serie)

        barcode = code128.Code128(
            value,
            barHeight=20 * mm,
            barWidth=0.4
        )

        # رسم الباركود
        barcode.drawOn(c, x, y)

        # اسم الجهاز
        c.setFont("Helvetica", 8)
        c.drawString(x, y - 15, eq.nom)

        # الرقم
        c.drawString(x, y - 25, value)

        y -= 80

        # صفحة جديدة إذا انتهى المكان
        if y < 50:
            c.showPage()
            y = 800

    c.save()

    return file_path