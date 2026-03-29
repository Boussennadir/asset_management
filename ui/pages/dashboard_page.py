"""
Page du tableau de bord.
Affiche les statistiques globales.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout
from PyQt6.QtCore import Qt


class StatCard(QFrame):
    """Carte de statistique pour le tableau de bord."""

    def __init__(self, title: str, value: str, color: str = "#3b82f6", icon: str = ""):
        super().__init__()
        self.setProperty("class", "stat-card")
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                padding: 20px;
            }}
        """)
        self.setMinimumHeight(130)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: #64748b; font-size: 13px; font-weight: 500;")
        layout.addWidget(title_label)

        value_label = QLabel(str(value))
        value_label.setStyleSheet(f"color: {color}; font-size: 36px; font-weight: 700;")
        layout.addWidget(value_label)

        self._value_label = value_label
        self._title_label = title_label

    def update_value(self, value: str, color: str = None):
        self._value_label.setText(str(value))
        if color:
            self._value_label.setStyleSheet(f"color: {color}; font-size: 36px; font-weight: 700;")


class DashboardPage(QWidget):
    """Page principale - Tableau de bord."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)

        # Titre
        header = QLabel("Tableau de bord")
        header.setObjectName("page_header")
        header.setStyleSheet("font-size: 24px; font-weight: 700; color: #1e293b; padding-bottom: 10px;")
        layout.addWidget(header)

        subtitle = QLabel("Vue d'ensemble de vos actifs")
        subtitle.setStyleSheet("color: #64748b; font-size: 14px; margin-bottom: 20px;")
        layout.addWidget(subtitle)

        # Grille de statistiques
        grid = QGridLayout()
        grid.setSpacing(16)

        self.card_total = StatCard("Total équipements", "0", "#3b82f6")
        self.card_actif = StatCard("Actifs", "0", "#16a34a")
        self.card_maintenance = StatCard("En maintenance", "0", "#ea580c")
        self.card_panne = StatCard("En panne", "0", "#dc2626")
        self.card_services = StatCard("Services", "0", "#8b5cf6")
        self.card_ss = StatCard("Sous-services", "0", "#06b6d4")

        grid.addWidget(self.card_total, 0, 0)
        grid.addWidget(self.card_actif, 0, 1)
        grid.addWidget(self.card_maintenance, 0, 2)
        grid.addWidget(self.card_panne, 1, 0)
        grid.addWidget(self.card_services, 1, 1)
        grid.addWidget(self.card_ss, 1, 2)

        layout.addLayout(grid)
        layout.addStretch()

    def refresh(self, stats: dict):
        """Met à jour les statistiques affichées."""
        self.card_total.update_value(str(stats.get("total", 0)))
        self.card_actif.update_value(str(stats.get("actif", 0)))
        self.card_maintenance.update_value(str(stats.get("maintenance", 0)))
        self.card_panne.update_value(str(stats.get("en_panne", 0)))
        self.card_services.update_value(str(stats.get("services", 0)))
        self.card_ss.update_value(str(stats.get("sous_services", 0)))
