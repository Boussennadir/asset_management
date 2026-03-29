"""
Page de gestion des services.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt

from services.service_manager import ServiceManager
from ui.dialogs.service_dialog import ServiceDialog


class ServicesPage(QWidget):
    """Page de gestion des services."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = ServiceManager()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)

        # En-tête
        header_layout = QHBoxLayout()
        header = QLabel("Gestion des services")
        header.setStyleSheet("font-size: 24px; font-weight: 700; color: #1e293b;")
        header_layout.addWidget(header)
        header_layout.addStretch()

        btn_add = QPushButton("＋ Ajouter un service")
        btn_add.clicked.connect(self._add_service)
        header_layout.addWidget(btn_add)
        layout.addLayout(header_layout)

        # Tableau
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Description", "Actif", "Équipements"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 100)
        layout.addWidget(self.table)

        # Boutons d'action
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_edit = QPushButton("✏️ Modifier")
        btn_edit.setObjectName("btn_secondary")
        btn_edit.clicked.connect(self._edit_service)
        btn_layout.addWidget(btn_edit)

        btn_delete = QPushButton("🗑️ Supprimer")
        btn_delete.setObjectName("btn_danger")
        btn_delete.clicked.connect(self._delete_service)
        btn_layout.addWidget(btn_delete)

        layout.addLayout(btn_layout)

    def refresh(self):
        """Recharge les données du tableau."""
        try:
            services = self.manager.get_all()
            self.table.setRowCount(len(services))
            for row, s in enumerate(services):
                self.table.setItem(row, 0, QTableWidgetItem(str(s.id)))
                self.table.setItem(row, 1, QTableWidgetItem(s.nom))
                self.table.setItem(row, 2, QTableWidgetItem(s.description))
                actif_item = QTableWidgetItem("✅ Oui" if s.actif else "❌ Non")
                actif_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 3, actif_item)
                count = self.manager.count_equipements(s.id)
                count_item = QTableWidgetItem(str(count))
                count_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 4, count_item)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les services :\n{e}")

    def _get_selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Information", "Veuillez sélectionner un service.")
            return None
        return int(self.table.item(row, 0).text())

    def _add_service(self):
        dlg = ServiceDialog(self)
        if dlg.exec():
            try:
                self.manager.create(dlg.get_data())
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de créer le service :\n{e}")

    def _edit_service(self):
        sid = self._get_selected_id()
        if sid is None: return
        service = self.manager.get_by_id(sid)
        dlg = ServiceDialog(self, service)
        if dlg.exec():
            try:
                self.manager.update(dlg.get_data())
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de modifier le service :\n{e}")

    def _delete_service(self):
        sid = self._get_selected_id()
        if sid is None: return
        count = self.manager.count_equipements(sid)
        if count > 0:
            QMessageBox.warning(self, "Suppression impossible",
                                f"Ce service possède {count} équipement(s).\n"
                                "Transférez-les d'abord avant de supprimer le service.")
            return
        reply = QMessageBox.question(self, "Confirmation",
                                     "Voulez-vous vraiment supprimer ce service ?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.manager.delete(sid)
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de supprimer le service :\n{e}")
