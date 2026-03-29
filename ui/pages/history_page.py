from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton
)
from PyQt6.QtCore import Qt
from services.history_manager import HistoryManager


class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()

        self.manager = HistoryManager()

        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Date", "Action", "Table", "Détails"
        ])

        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)

        refresh_btn = QPushButton("🔄 Rafraîchir")
        refresh_btn.clicked.connect(self.load_data)
        layout.addWidget(refresh_btn)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)

        rows = self.manager.get_all()
        self.table.setRowCount(len(rows))

        for i, r in enumerate(rows):
            for j in range(4):
                item = QTableWidgetItem(str(r[j]))

                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                self.table.setItem(i, j, item)