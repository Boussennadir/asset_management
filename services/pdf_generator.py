"""
PDF Generator - Décharge de transfert d'équipement
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
from pathlib import Path
import os
import re


# ===============================
# 📁 Dossier Documents
# ===============================
def get_pdf_directory():
    folder = Path.home() / "Documents" / "AssetApp" / "Decharges"
    folder.mkdir(parents=True, exist_ok=True)
    return str(folder)


# ===============================
# 🔢 Fichier compteur
# ===============================
def get_counter_file():
    folder = Path.home() / "Documents" / "AssetApp"
    folder.mkdir(parents=True, exist_ok=True)
    return str(folder / "reference_counter.txt")


# ===============================
# 🔢 Génération référence (SAFE)
# ===============================
def generate_reference():
    counter_file = get_counter_file()

    try:
        if not os.path.exists(counter_file):
            with open(counter_file, "w") as f:
                f.write("1")
            return "00001"

        with open(counter_file, "r") as f:
            content = f.read().strip()
            current = int(content) if content else 0

        new = current + 1

        with open(counter_file, "w") as f:
            f.write(str(new))

        return f"{new:05d}"

    except Exception:
        # fallback في حالة خطأ
        return datetime.now().strftime("%Y%m%d%H%M%S")


# ===============================
# 🧹 Nettoyer nom fichier
# ===============================
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)


# ===============================
# 📄 Génération PDF
# ===============================
def generate_transfer_pdf(equipement, service_name, motif):
    # 🧹 تنظيف الاسم
    safe_name = sanitize_filename(equipement.nom)

    # 📁 مسار الحفظ
    filename = f"decharge_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_path = os.path.join(get_pdf_directory(), filename)

    # 📄 إنشاء PDF
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    ref = generate_reference()
    today = datetime.now().strftime("%d/%m/%Y")

    # ===== HEADER =====
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(
        width / 2, height - 50,
        "REPUBLIQUE ALGERIENNE DEMOCRATIQUE ET POPULAIRE"
    )

    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 75, "Centre Des Impôts Batna")

    c.drawCentredString(
        width / 2, height - 95,
        "Service d’Informatique et de la gestion des Moyennes"
    )

    # ===== TITLE =====
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(width / 2, height - 130, "DECHARGE")

    # ===== REF + DATE =====
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 160, f"N°: CDI-{ref}")
    c.drawRightString(width - 50, height - 160, f"Date: {today}")

    # ===== TEXT =====
    c.drawString(
        50, height - 190,
        "Je soussigné(e) certifie avoir reçu les équipements suivants :"
    )

    # ===== TABLE =====
    data = [
        ["Désignation", "N° série", "Observation"],
        [
            equipement.nom,
            str(equipement.numero_serie),
            motif if motif else "-"
        ]
    ]

    table = Table(data, colWidths=[200, 120, 150])

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    table.wrapOn(c, width, height)
    table.drawOn(c, 50, height - 260)

    # ===== LOCATION =====
    c.drawString(
        50, height - 300,
        f"Reçu à: {service_name} le: {today}"
    )

    # ===== SIGNATURE =====
    c.drawString(50, height - 340, "Nom et Prénom: ................................................")
    c.drawString(50, height - 370, "Grade / Fonction: ..............................................")
    c.drawString(50, height - 400, "Signature: ......................................................")

    # ===== SAVE =====
    c.save()

    # ✅ Vérification
    if not os.path.exists(file_path):
        raise Exception("Erreur: PDF non créé")

    if os.path.getsize(file_path) == 0:
        raise Exception("Erreur: PDF vide")

    return file_path