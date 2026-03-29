"""
Dialogue d'ajout / modification d'un service.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit,
    QDialogButtonBox, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt
from models.models import Service


class ServiceDialog(QDialog):
    """Dialogue pour créer ou modifier un service."""

    def __init__(self, parent=None, service: Service = None):
        super().__init__(parent)
        self.service = service
        self.setWindowTitle("Modifier le service" if service else "Nouveau service")
        self.setMinimumWidth(450)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        form = QFormLayout()
        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Nom du service")
        form.addRow("Nom :", self.nom_input)

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Description (optionnel)")
        self.desc_input.setMaximumHeight(100)
        form.addRow("Description :", self.desc_input)

        self.actif_check = QCheckBox("Actif")
        self.actif_check.setChecked(True)
        form.addRow("Statut :", self.actif_check)

        layout.addLayout(form)

        # Préremplir si modification
        if self.service:
            self.nom_input.setText(self.service.nom)
            self.desc_input.setPlainText(self.service.description)
            self.actif_check.setChecked(self.service.actif)

        # Boutons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Enregistrer")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Annuler")
        buttons.accepted.connect(self._validate)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _validate(self):
        nom = self.nom_input.text().strip()
        if not nom:
            QMessageBox.warning(self, "Erreur de validation", "Le nom du service est obligatoire.")
            return
        if len(nom) > 150:
            QMessageBox.warning(self, "Erreur de validation", "Le nom ne doit pas dépasser 150 caractères.")
            return
        self.accept()

    def get_data(self) -> Service:
        """Retourne le service avec les données saisies."""
        s = self.service if self.service else Service()
        s.nom = self.nom_input.text().strip()
        s.description = self.desc_input.toPlainText().strip()
        s.actif = self.actif_check.isChecked()
        return s
