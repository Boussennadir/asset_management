"""
Point d'entrée de l'application Asset Management System.
Cabinet fiscal — Gestion des actifs.
"""

import sys
import os
import logging
from database.db_manager import DatabaseManager

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from ui.main_window import MainWindow

def ensure_categories_exist():
    db = DatabaseManager()

    rows = db.fetch_all("SELECT COUNT(*) FROM categories")
    if rows[0][0] == 0:
        db.execute("""
            INSERT INTO categories (nom) VALUES
            (N'Informatique'),
            (N'Mobilier'),
            (N'Électronique'),
            (N'Véhicule'),
            (N'Autre')
        """)
        db.connection.commit()
        
def setup_logging():
    """Configure le système de journalisation."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("app.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )


def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Démarrage de l'application Asset Management System")
    ensure_categories_exist() 
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
