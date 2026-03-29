"""
Dialogue d'ajout / modification d'un équipement.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit,
    QDialogButtonBox, QMessageBox, QComboBox, QDateEdit
)
from PyQt6.QtCore import QDate
from models.models import Equipement
from services.service_manager import ServiceManager
from services.sous_service_manager import SousServiceManager
from services.category_manager import CategoryManager


class EquipementDialog(QDialog):
    """Dialogue pour créer ou modifier un équipement."""

    STATUTS = ["Actif", "Maintenance", "En panne"]

    def __init__(self, parent=None, equipement: Equipement = None):
        super().__init__(parent)
        self.equipement = equipement
        self.setWindowTitle("Modifier l'équipement" if equipement else "Nouvel équipement")
        self.setMinimumWidth(500)
        self._services = ServiceManager().get_all(actif_only=True)
        self._categories = CategoryManager().get_all()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Nom
        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Nom de l'équipement")
        form.addRow("Nom :", self.nom_input)

        # Catégorie
        self.cat_combo = QComboBox()
        for c in self._categories:
            self.cat_combo.addItem(c.nom, c.id)
        form.addRow("Catégorie :", self.cat_combo)

        # Numéro de série
        self.serie_input = QLineEdit()
        self.serie_input.setPlaceholderText("Numéro de série (optionnel)")
        form.addRow("N° de série :", self.serie_input)

        # Date d'achat
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        form.addRow("Date d'achat :", self.date_input)

        # Statut
        self.statut_combo = QComboBox()
        self.statut_combo.addItems(self.STATUTS)
        form.addRow("Statut :", self.statut_combo)

        # Service
        self.service_combo = QComboBox()
        for s in self._services:
            self.service_combo.addItem(s.nom, s.id)
        self.service_combo.currentIndexChanged.connect(self._on_service_changed)
        form.addRow("Service :", self.service_combo)

        # Sous-service
        self.ss_combo = QComboBox()
        self.ss_combo.addItem("— Aucun —", None)
        form.addRow("Sous-service :", self.ss_combo)

        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Notes (optionnel)")
        self.notes_input.setMaximumHeight(80)
        form.addRow("Notes :", self.notes_input)

        layout.addLayout(form)

        # Préremplir si modification
        if self.equipement:
            self.nom_input.setText(self.equipement.nom)
            idx = self.cat_combo.findData(self.equipement.categorie_id)
            if idx >= 0: self.cat_combo.setCurrentIndex(idx)
            self.serie_input.setText(self.equipement.numero_serie)
            if self.equipement.date_achat:
                self.date_input.setDate(QDate(
                    self.equipement.date_achat.year,
                    self.equipement.date_achat.month,
                    self.equipement.date_achat.day
                ))
            s_idx = self.statut_combo.findText(self.equipement.statut)
            if s_idx >= 0: self.statut_combo.setCurrentIndex(s_idx)
            sv_idx = self.service_combo.findData(self.equipement.service_id)
            if sv_idx >= 0: self.service_combo.setCurrentIndex(sv_idx)
            self.notes_input.setPlainText(self.equipement.notes)

        # Charger sous-services initiaux
        self._on_service_changed()

        # Sélectionner le sous-service après chargement
        if self.equipement and self.equipement.sous_service_id:
            ss_idx = self.ss_combo.findData(self.equipement.sous_service_id)
            if ss_idx >= 0: self.ss_combo.setCurrentIndex(ss_idx)

        # Boutons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Enregistrer")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Annuler")
        buttons.accepted.connect(self._validate)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _on_service_changed(self):
        """Recharge les sous-services quand le service change."""
        self.ss_combo.clear()
        self.ss_combo.addItem("— Aucun —", None)
        service_id = self.service_combo.currentData()
        if service_id:
            sous_services = SousServiceManager().get_all(service_id=service_id)
            for ss in sous_services:
                self.ss_combo.addItem(ss.nom, ss.id)

    def _validate(self):
        if not self.nom_input.text().strip():
            QMessageBox.warning(self, "Erreur de validation", "Le nom de l'équipement est obligatoire.")
            return
        if self.service_combo.count() == 0:
            QMessageBox.warning(self, "Erreur", "Aucun service disponible. Créez d'abord un service.")
            return
        self.accept()

    def get_data(self) -> Equipement:
        eq = self.equipement if self.equipement else Equipement()
        eq.nom = self.nom_input.text().strip()
        eq.categorie_id = self.cat_combo.currentData()
        eq.numero_serie = self.serie_input.text().strip()
        d = self.date_input.date()
        eq.date_achat = d.toPyDate() if d.isValid() else None
        eq.statut = self.statut_combo.currentText()
        eq.service_id = self.service_combo.currentData()
        eq.sous_service_id = self.ss_combo.currentData()
        eq.notes = self.notes_input.toPlainText().strip()
        return eq
