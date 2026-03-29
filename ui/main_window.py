"""
Fenêtre principale de l'application.
Contient la barre latérale et le QStackedWidget pour la navigation.
"""

import logging
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

from database.db_manager import DatabaseManager
from services.asset_manager import AssetManager
from ui.pages.dashboard_page import DashboardPage
from ui.pages.services_page import ServicesPage
from ui.pages.sous_services_page import SousServicesPage
from ui.pages.equipements_page import EquipementsPage
from resources.styles import MAIN_STYLE
from ui.pages.history_page import HistoryPage

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Fenêtre principale de l'application Asset Management."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Actifs — Cabinet Fiscal")
        self.setMinimumSize(QSize(1100, 700))
        self.resize(1280, 800)
        self.setStyleSheet(MAIN_STYLE)

        self.db = DatabaseManager()
        self._connect_db()
        self._init_ui()
        self._navigate(0)

    def _connect_db(self):
        """Tente la connexion à la base de données."""
        if not self.db.connect():
            QMessageBox.critical(
                self, "Erreur de connexion",
                "Impossible de se connecter à la base de données SQL Server.\n\n"
                "Vérifiez votre fichier config.ini et assurez-vous que :\n"
                "• SQL Server est démarré\n"
                "• Le driver ODBC 17 est installé\n"
                "• Les paramètres de connexion sont corrects"
            )

    def _init_ui(self):
        """Initialise l'interface utilisateur."""
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # === Sidebar ===
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Logo / Titre
        title = QLabel("📊 Gestion Actifs")
        title.setObjectName("sidebar_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title)

        # Séparateur
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #334155; max-height: 1px;")
        sidebar_layout.addWidget(sep)

        # Boutons de navigation
        self.nav_buttons = []
        nav_items = [
            ("📊  Tableau de bord", 0),
            ("🏢  Services", 1),
            ("📁  Sous-services", 2),
            ("💻  Équipements", 3),
            ("🕘  Historique", 4),
        ]

        for text, index in nav_items:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, idx=index: self._navigate(idx))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()

        # Info connexion
        mode_label = QLabel("🔗 Mode: local")
        mode_label.setStyleSheet("color: #64748b; font-size: 11px; padding: 12px;")
        mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(mode_label)

        main_layout.addWidget(sidebar)

        # === Pages (QStackedWidget) ===
        self.pages = QStackedWidget()
        self.dashboard_page = DashboardPage()
        self.services_page = ServicesPage()
        self.sous_services_page = SousServicesPage()
        self.equipements_page = EquipementsPage()
        self.history_page = HistoryPage()

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.services_page)
        self.pages.addWidget(self.sous_services_page)
        self.pages.addWidget(self.equipements_page)
        self.pages.addWidget(self.history_page)
        main_layout.addWidget(self.pages, 1)

    def _navigate(self, index: int):
        """Change la page active et met à jour la sidebar."""
        self.pages.setCurrentIndex(index)

        # Mettre à jour l'état des boutons
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
            btn.setProperty("active", "true" if i == index else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        # Rafraîchir la page active
        try:
            if index == 0:
                stats = AssetManager().get_stats()
                self.dashboard_page.refresh(stats)
            elif index == 1:
                self.services_page.refresh()
            elif index == 2:
                self.sous_services_page.refresh()
            elif index == 3:
                self.equipements_page.refresh()
            elif index == 4:
                self.history_page.load_data

        except Exception as e:
            logger.error("Erreur lors du rafraîchissement : %s", e)

    def closeEvent(self, event):
        """Ferme la connexion à la base de données à la fermeture."""
        self.db.disconnect()
        event.accept()
