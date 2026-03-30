from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime


def generate_transfer_pdf(equipement, service_name, motif):
    file_path = os.path.join(os.getcwd(), "transfer_generated.pdf")

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # ===== HEADER =====
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 50, "REPUBLIQUE ALGERIENNE DEMOCRATIQUE ET POPULAIRE")

    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 80, "Centre Des Impôts Batna")

    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, height - 110, "DECHARGE")

    # ===== INFO =====
    today = datetime.now().strftime("%d/%m/%Y")

    c.setFont("Helvetica", 11)
    c.drawString(50, height - 150, f"Date: {today}")
    c.drawString(50, height - 170, f"Service destination: {service_name}")

    # ===== TABLE =====
    c.drawString(50, height - 210, "Designation:")
    c.drawString(200, height - 210, equipement.nom)

    c.drawString(50, height - 230, "Numero de serie:")
    c.drawString(200, height - 230, str(equipement.numero_serie))

    c.drawString(50, height - 250, "Observation:")
    c.drawString(200, height - 250, motif if motif else "-")

    # ===== SIGNATURE =====
    c.drawString(50, height - 320, "Nom et Prenom: ________________________")
    c.drawString(50, height - 350, "Signature: _____________________________")

    c.save()

    return file_path