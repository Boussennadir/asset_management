"""
Page de gestion des équipements.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QLabel, QLineEdit,
    QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from services.asset_manager import AssetManager
from services.service_manager import ServiceManager
from ui.dialogs.equipement_dialog import EquipementDialog
from ui.dialogs.transfer_dialog import TransferDialog
from services.barcode_generator import generate_barcode_pdf
import os
from PyQt6.QtWidgets import QMessageBox

STATUS_COLORS = {
    "Actif": QColor("#dcfce7"),
    "Maintenance": QColor("#ffedd5"),
    "En panne": QColor("#fee2e2"),
}

STATUS_TEXT_COLORS = {
    "Actif": QColor("#16a34a"),
    "Maintenance": QColor("#ea580c"),
    "En panne": QColor("#dc2626"),
}


class EquipementsPage(QWidget):
    """Page de gestion des équipements."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = AssetManager()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)

        # En-tête
        header_layout = QHBoxLayout()
        header = QLabel("Gestion des équipements")
        header.setStyleSheet("font-size: 24px; font-weight: 700; color: #1e293b;")
        header_layout.addWidget(header)
        header_layout.addStretch()

        btn_add = QPushButton("＋ Ajouter un équipement")
        btn_add.clicked.connect(self._add)
        header_layout.addWidget(btn_add)
        layout.addLayout(header_layout)

        # Barre de filtres
        filter_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setObjectName("search_bar")
        self.search_input.setPlaceholderText("🔍 Rechercher par nom, n° série ou service...")
        self.search_input.textChanged.connect(self._apply_filters)
        filter_layout.addWidget(self.search_input)

        self.filter_statut = QComboBox()
        self.filter_statut.addItem("Tous les statuts", None)
        self.filter_statut.addItems(["Actif", "Maintenance", "En panne"])
        self.filter_statut.currentIndexChanged.connect(self._apply_filters)
        filter_layout.addWidget(self.filter_statut)

        self.filter_service = QComboBox()
        self.filter_service.addItem("Tous les services", None)
        self._load_service_filter()
        self.filter_service.currentIndexChanged.connect(self._apply_filters)
        filter_layout.addWidget(self.filter_service)

        layout.addLayout(filter_layout)

        # Tableau
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nom", "Catégorie", "N° Série", "Statut", "Service", "Sous-service", "Date d'achat"
        ])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 130)
        self.table.setColumnWidth(4, 110)
        self.table.setColumnWidth(5, 140)
        self.table.setColumnWidth(6, 140)
        self.table.setColumnWidth(7, 110)
        layout.addWidget(self.table)

        # Boutons d'action
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_barcode = QPushButton("🏷️ Code Barre")
        btn_barcode.setObjectName("btn_secondary")
        btn_barcode.clicked.connect(self._generate_barcode)
        btn_layout.addWidget(btn_barcode)
        
        btn_transfer = QPushButton("🔄 Transférer")
        btn_transfer.setObjectName("btn_success")
        btn_transfer.setStyleSheet("background-color: #8b5cf6;")
        btn_transfer.clicked.connect(self._transfer)
        btn_layout.addWidget(btn_transfer)

        btn_edit = QPushButton("✏️ Modifier")
        btn_edit.setObjectName("btn_secondary")
        btn_edit.clicked.connect(self._edit)
        btn_layout.addWidget(btn_edit)

        btn_delete = QPushButton("🗑️ Supprimer")
        btn_delete.setObjectName("btn_danger")
        btn_delete.clicked.connect(self._delete)
        btn_layout.addWidget(btn_delete)

        layout.addLayout(btn_layout)

    def _load_service_filter(self):
        """Charge les services dans le filtre."""

        try:
            self.filter_service.blockSignals(True)

            current = self.filter_service.currentData()

            self.filter_service.clear()
            self.filter_service.addItem("Tous les services", None)

            for s in ServiceManager().get_all(actif_only=True):
                self.filter_service.addItem(s.nom, s.id)

            if current:
                index = self.filter_service.findData(current)
                if index >= 0:
                    self.filter_service.setCurrentIndex(index)

            self.filter_service.blockSignals(False)

        except Exception:
            self.filter_service.blockSignals(False)

    def _get_filters(self) -> dict:
        filters = {}
        text = self.search_input.text().strip()
        if text:
            filters["recherche"] = text
        statut = self.filter_statut.currentText()
        if statut != "Tous les statuts":
            filters["statut"] = statut
        service_id = self.filter_service.currentData()
        if service_id:
            filters["service_id"] = service_id
        return filters

    def _apply_filters(self):
        self.refresh()

    def refresh(self):
        try:
            self._load_service_filter()
            filters = self._get_filters()
            equipements = self.manager.get_all(filters if filters else None)
            self.table.setRowCount(len(equipements))
            for row, eq in enumerate(equipements):
                self.table.setItem(row, 0, QTableWidgetItem(str(eq.id)))
                self.table.setItem(row, 1, QTableWidgetItem(eq.nom))
                self.table.setItem(row, 2, QTableWidgetItem(eq.categorie_nom))
                self.table.setItem(row, 3, QTableWidgetItem(eq.numero_serie))

                # Statut avec couleur
                statut_item = QTableWidgetItem(eq.statut)
                statut_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                bg = STATUS_COLORS.get(eq.statut)
                fg = STATUS_TEXT_COLORS.get(eq.statut)
                if bg: statut_item.setBackground(bg)
                if fg: statut_item.setForeground(fg)
                self.table.setItem(row, 4, statut_item)

                self.table.setItem(row, 5, QTableWidgetItem(eq.service_nom))
                self.table.setItem(row, 6, QTableWidgetItem(eq.sous_service_nom))
                date_str = eq.date_achat.strftime("%d/%m/%Y") if eq.date_achat else ""
                self.table.setItem(row, 7, QTableWidgetItem(date_str))
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les équipements :\n{e}")

    def _get_selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Information", "Veuillez sélectionner un équipement.")
            return None
        return int(self.table.item(row, 0).text())

    def _add(self):
        dlg = EquipementDialog(self)
        if dlg.exec():
            try:
                self.manager.create(dlg.get_data())
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la création :\n{e}")

    def _edit(self):
        eid = self._get_selected_id()
        if eid is None: return
        eq = self.manager.get_by_id(eid)
        dlg = EquipementDialog(self, eq)
        if dlg.exec():
            try:
                self.manager.update(dlg.get_data())
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la modification :\n{e}")

    def _delete(self):
        eid = self._get_selected_id()
        if eid is None: return
        reply = QMessageBox.question(self, "Confirmation",
                                     "Voulez-vous vraiment supprimer cet équipement ?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.manager.delete(eid)
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression :\n{e}")

    def _transfer(self):
        eid = self._get_selected_id()
        if eid is None: return
        eq = self.manager.get_by_id(eid)
        dlg = TransferDialog(self, eq)
        if dlg.exec():
            try:
                self.manager.transfer(eid, dlg.get_new_service_id(),
                                      dlg.get_new_sous_service_id(), dlg.get_motif())
                self.refresh()
                QMessageBox.information(self, "Succès", "L'équipement a été transféré avec succès.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors du transfert :\n{e}")
    
    def _generate_barcode(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un équipement.")
            return

        try:
            eid = int(self.table.item(row, 0).text())
            eq = self.manager.get_by_id(eid)

            # 🔥 توليد PDF لعنصر واحد
            pdf_path = generate_barcode_pdf(eq)

            QMessageBox.information(
                self,
                "Succès",
                f"Code barre généré avec succès ✅"
            )

        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))
