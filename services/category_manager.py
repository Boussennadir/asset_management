"""
Gestionnaire des catégories.
"""

from typing import List
from database.db_manager import DatabaseManager
from models.models import Categorie


class CategoryManager:
    """Gère les catégories d'équipements."""

    def __init__(self):
        self.db = DatabaseManager()

    def get_all(self) -> List[Categorie]:
        rows = self.db.fetch_all("SELECT id, nom FROM categories ORDER BY nom")
        return [Categorie(id=r[0], nom=r[1]) for r in rows]

    def create(self, nom: str) -> int:
        cursor = self.db.execute(
            "INSERT INTO categories (nom) OUTPUT INSERTED.id VALUES (?)", (nom.strip(),)
        )
        new_id = cursor.fetchone()[0]

        self.db.connection.commit()
        return new_id
