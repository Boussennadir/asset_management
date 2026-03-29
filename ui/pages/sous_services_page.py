"""
Page de gestion des sous-services.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt

from services.sous_service_manager import SousServiceManager
from ui.dialogs.sous_service_dialog import SousServiceDialog


class SousServicesPage(QWidget):
    """Page de gestion des sous-services."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = SousServiceManager()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)

        header_layout = QHBoxLayout()
        header = QLabel("Gestion des sous-services")
        header.setStyleSheet("font-size: 24px; font-weight: 700; color: #1e293b;")
        header_layout.addWidget(header)
        header_layout.addStretch()

        btn_add = QPushButton("＋ Ajouter un sous-service")
        btn_add.clicked.connect(self._add)
        header_layout.addWidget(btn_add)
        layout.addLayout(header_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Service parent", "Description", "Actif"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(2, 180)
        self.table.setColumnWidth(4, 80)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_edit = QPushButton("✏️ Modifier")
        btn_edit.setObjectName("btn_secondary")
        btn_edit.clicked.connect(self._edit)
        btn_layout.addWidget(btn_edit)
        btn_delete = QPushButton("🗑️ Supprimer")
        btn_delete.setObjectName("btn_danger")
        btn_delete.clicked.connect(self._delete)
        btn_layout.addWidget(btn_delete)
        layout.addLayout(btn_layout)

    def refresh(self):
        try:
            items = self.manager.get_all()
            self.table.setRowCount(len(items))
            for row, ss in enumerate(items):
                self.table.setItem(row, 0, QTableWidgetItem(str(ss.id)))
                self.table.setItem(row, 1, QTableWidgetItem(ss.nom))
                self.table.setItem(row, 2, QTableWidgetItem(ss.service_nom))
                self.table.setItem(row, 3, QTableWidgetItem(ss.description))
                actif = QTableWidgetItem("✅ Oui" if ss.actif else "❌ Non")
                actif.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 4, actif)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les sous-services :\n{e}")

    def _get_selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Information", "Veuillez sélectionner un sous-service.")
            return None
        return int(self.table.item(row, 0).text())

    def _add(self):
        dlg = SousServiceDialog(self)
        if dlg.exec():
            try:
                self.manager.create(dlg.get_data())
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la création :\n{e}")

    def _edit(self):
        sid = self._get_selected_id()
        if sid is None: return
        ss = self.manager.get_by_id(sid)
        dlg = SousServiceDialog(self, ss)
        if dlg.exec():
            try:
                self.manager.update(dlg.get_data())
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la modification :\n{e}")

    def _delete(self):
        sid = self._get_selected_id()
        if sid is None: return
        reply = QMessageBox.question(self, "Confirmation",
                                     "Voulez-vous vraiment supprimer ce sous-service ?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.manager.delete(sid)
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression :\n{e}")
