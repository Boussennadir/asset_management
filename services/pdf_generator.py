"""
PDF Generator - Décharge de transfert d'équipement
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
import random
import os


# ===============================
# 🔢 Génération numéro référence
# ===============================
import os

COUNTER_FILE = "reference_counter.txt"


def generate_reference():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("1")
        return "0"

    with open(COUNTER_FILE, "r") as f:
        current = int(f.read().strip())

    new = current + 1

    with open(COUNTER_FILE, "w") as f:
        f.write(str(new))

    return str(new)

# ===============================
# 📄 Génération PDF
# ===============================
def generate_transfer_pdf(equipement, service_name, motif, file_path):
    """
    Génère une décharge PDF professionnelle

    :param equipement: objet Equipement
    :param service_name: nom du service destination
    :param motif: motif du transfert
    :param file_path: chemin complet du fichier PDF
    """

    # ✅ Sécurité: créer dossier si inexistant
    folder = os.path.dirname(file_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    # ===============================
    # 📄 Création document
    # ===============================
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # ===============================
    # 🔢 Référence + Date
    # ===============================
    ref = generate_reference()
    today = datetime.now().strftime("%d/%m/%Y")

    # ===============================
    # 🏛️ HEADER
    # ===============================
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

    # ===============================
    # 📌 TITRE
    # ===============================
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(width / 2, height - 130, "DECHARGE")

    # ===============================
    # 📌 Référence + Date
    # ===============================
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 160, f"N°: {ref}")
    c.drawRightString(width - 50, height - 160, f"Date: {today}")

    # ===============================
    # 📄 TEXTE INTRO
    # ===============================
    c.drawString(
        50, height - 190,
        "Je soussigné(e) certifie avoir reçu les équipements suivants :"
    )

    # ===============================
    # 📋 TABLEAU
    # ===============================
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

    # ===============================
    # 📍 Lieu de réception
    # ===============================
    c.drawString(
        50, height - 300,
        f"Reçu à: {service_name} le: {today}"
    )

    # ===============================
    # ✍️ SIGNATURES
    # ===============================
    c.drawString(
        50, height - 340,
        "Nom et Prénom: ................................................"
    )

    c.drawString(
        50, height - 370,
        "Grade / Fonction: .............................................."
    )

    c.drawString(
        50, height - 400,
        "Signature: ......................................................"
    )

    # ===============================
    # 💾 Sauvegarde
    # ===============================
    c.save()

    # ✅ Vérification
    if not os.path.exists(file_path):
        raise Exception("Erreur: le fichier PDF n'a pas été créé.")

    if os.path.getsize(file_path) == 0:
        raise Exception("Erreur: le fichier PDF est vide.")

    return file_path