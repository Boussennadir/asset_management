"""
Dialogue de transfert d'un équipement.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QComboBox, QTextEdit,
    QDialogButtonBox, QMessageBox, QLabel
)
from models.models import Equipement
from services.service_manager import ServiceManager
from services.sous_service_manager import SousServiceManager


class TransferDialog(QDialog):
    """Dialogue pour transférer un équipement vers un autre service."""

    def __init__(self, parent=None, equipement: Equipement = None):
        super().__init__(parent)
        self.equipement = equipement
        self.setWindowTitle("Transférer l'équipement")
        self.setMinimumWidth(450)
        self._services = ServiceManager().get_all(actif_only=True)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # Info équipement
        info = QLabel(f"<b>Équipement :</b> {self.equipement.nom}<br>"
                      f"<b>Service actuel :</b> {self.equipement.service_nom}")
        layout.addWidget(info)

        form = QFormLayout()

        self.service_combo = QComboBox()
        for s in self._services:
            self.service_combo.addItem(s.nom, s.id)
        self.service_combo.currentIndexChanged.connect(self._on_service_changed)
        form.addRow("Nouveau service :", self.service_combo)

        self.ss_combo = QComboBox()
        self.ss_combo.addItem("— Aucun —", None)
        form.addRow("Nouveau sous-service :", self.ss_combo)

        self.motif_input = QTextEdit()
        self.motif_input.setPlaceholderText("Motif du transfert (optionnel)")
        self.motif_input.setMaximumHeight(80)
        form.addRow("Motif :", self.motif_input)

        layout.addLayout(form)
        self._on_service_changed()

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Transférer")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Annuler")
        buttons.accepted.connect(self._validate)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _on_service_changed(self):
        self.ss_combo.clear()
        self.ss_combo.addItem("— Aucun —", None)
        service_id = self.service_combo.currentData()
        if service_id:
            for ss in SousServiceManager().get_all(service_id=service_id):
                self.ss_combo.addItem(ss.nom, ss.id)

    def _validate(self):
        new_service = self.service_combo.currentData()
        new_ss = self.ss_combo.currentData()
        if new_service == self.equipement.service_id and new_ss == self.equipement.sous_service_id:
            QMessageBox.warning(self, "Erreur", "L'équipement est déjà dans ce service/sous-service.")
            return
        self.accept()

    def get_new_service_id(self) -> int:
        return self.service_combo.currentData()

    def get_new_sous_service_id(self):
        return self.ss_combo.currentData()

    def get_motif(self) -> str:
        return self.motif_input.toPlainText().strip()
