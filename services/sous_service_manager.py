"""
Gestionnaire des sous-services (logique métier).
"""

import logging
from typing import List, Optional

from database.db_manager import DatabaseManager
from models.models import SousService

logger = logging.getLogger(__name__)


class SousServiceManager:
    """Gère les opérations CRUD sur les sous-services."""

    def __init__(self):
        self.db = DatabaseManager()

    def get_all(self, service_id: Optional[int] = None) -> List[SousService]:
        """Récupère tous les sous-services, éventuellement filtrés par service."""
        query = """
            SELECT ss.id, ss.nom, ss.service_id, s.nom, ss.description, ss.date_creation, ss.actif
            FROM sous_services ss
            JOIN services s ON ss.service_id = s.id
        """
        params = ()
        if service_id:
            query += " WHERE ss.service_id = ?"
            params = (service_id,)
        query += " ORDER BY s.nom, ss.nom"
        rows = self.db.fetch_all(query, params)
        return [
            SousService(id=r[0], nom=r[1], service_id=r[2], service_nom=r[3],
                        description=r[4] or "", date_creation=r[5], actif=bool(r[6]))
            for r in rows
        ]

    def get_by_id(self, ss_id: int) -> Optional[SousService]:
        row = self.db.fetch_one(
            """SELECT ss.id, ss.nom, ss.service_id, s.nom, ss.description, ss.date_creation, ss.actif
               FROM sous_services ss JOIN services s ON ss.service_id = s.id WHERE ss.id = ?""",
            (ss_id,)
        )
        if row:
            return SousService(id=row[0], nom=row[1], service_id=row[2], service_nom=row[3],
                               description=row[4] or "", date_creation=row[5], actif=bool(row[6]))
        return None

    def create(self, ss: SousService) -> int:
        cursor = self.db.execute(
            "INSERT INTO sous_services (nom, service_id, description) OUTPUT INSERTED.id VALUES (?, ?, ?)",
            (ss.nom.strip(), ss.service_id, ss.description.strip())
        )
        new_id = cursor.fetchone()[0]
        self.db.connection.commit()
        self.db.log_action("sous_services", "INSERT", new_id, f"Création du sous-service '{ss.nom}'")
        return new_id

    def update(self, ss: SousService):
        self.db.execute(
            "UPDATE sous_services SET nom = ?, service_id = ?, description = ?, actif = ? WHERE id = ?",
            (ss.nom.strip(), ss.service_id, ss.description.strip(), ss.actif, ss.id)
        )
        self.db.connection.commit()
        self.db.log_action("sous_services", "UPDATE", ss.id, f"Modification du sous-service '{ss.nom}'")

    def delete(self, ss_id: int):
        ss = self.get_by_id(ss_id)
        nom = ss.nom if ss else "?"
        self.db.execute("DELETE FROM sous_services WHERE id = ?", (ss_id,))
        self.db.connection.commit()
        self.db.log_action("sous_services", "DELETE", ss_id, f"Suppression du sous-service '{nom}'")
