"""
Dialogue d'ajout / modification d'un sous-service.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit,
    QDialogButtonBox, QMessageBox, QCheckBox, QComboBox
)
from models.models import SousService
from services.service_manager import ServiceManager


class SousServiceDialog(QDialog):
    """Dialogue pour créer ou modifier un sous-service."""

    def __init__(self, parent=None, sous_service: SousService = None):
        super().__init__(parent)
        self.sous_service = sous_service
        self.setWindowTitle("Modifier le sous-service" if sous_service else "Nouveau sous-service")
        self.setMinimumWidth(450)
        self._services = ServiceManager().get_all(actif_only=True)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Nom du sous-service")
        form.addRow("Nom :", self.nom_input)

        self.service_combo = QComboBox()
        for s in self._services:
            self.service_combo.addItem(s.nom, s.id)
        form.addRow("Service parent :", self.service_combo)

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Description (optionnel)")
        self.desc_input.setMaximumHeight(100)
        form.addRow("Description :", self.desc_input)

        self.actif_check = QCheckBox("Actif")
        self.actif_check.setChecked(True)
        form.addRow("Statut :", self.actif_check)

        layout.addLayout(form)

        if self.sous_service:
            self.nom_input.setText(self.sous_service.nom)
            self.desc_input.setPlainText(self.sous_service.description)
            self.actif_check.setChecked(self.sous_service.actif)
            idx = self.service_combo.findData(self.sous_service.service_id)
            if idx >= 0:
                self.service_combo.setCurrentIndex(idx)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Enregistrer")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Annuler")
        buttons.accepted.connect(self._validate)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _validate(self):
        if not self.nom_input.text().strip():
            QMessageBox.warning(self, "Erreur de validation", "Le nom du sous-service est obligatoire.")
            return
        if self.service_combo.count() == 0:
            QMessageBox.warning(self, "Erreur", "Aucun service disponible. Créez d'abord un service.")
            return
        self.accept()

    def get_data(self) -> SousService:
        ss = self.sous_service if self.sous_service else SousService()
        ss.nom = self.nom_input.text().strip()
        ss.service_id = self.service_combo.currentData()
        ss.description = self.desc_input.toPlainText().strip()
        ss.actif = self.actif_check.isChecked()
        return ss
