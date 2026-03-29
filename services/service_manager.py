"""
Gestionnaire des services (logique métier).
"""

import logging
from typing import List, Optional

from database.db_manager import DatabaseManager
from models.models import Service

logger = logging.getLogger(__name__)


class ServiceManager:
    """Gère les opérations CRUD sur les services."""

    def __init__(self):
        self.db = DatabaseManager()

    def get_all(self, actif_only: bool = False) -> List[Service]:
        """Récupère tous les services."""
        query = "SELECT id, nom, description, date_creation, actif FROM services"
        if actif_only:
            query += " WHERE actif = 1"
        query += " ORDER BY nom"
        rows = self.db.fetch_all(query)
        return [Service(id=r[0], nom=r[1], description=r[2] or "", date_creation=r[3], actif=bool(r[4])) for r in rows]

    def get_by_id(self, service_id: int) -> Optional[Service]:
        """Récupère un service par son ID."""
        row = self.db.fetch_one("SELECT id, nom, description, date_creation, actif FROM services WHERE id = ?", (service_id,))
        if row:
            return Service(id=row[0], nom=row[1], description=row[2] or "", date_creation=row[3], actif=bool(row[4]))
        return None

    def create(self, service: Service) -> int:
        """Crée un nouveau service. Retourne l'ID."""
        cursor = self.db.execute(
            "INSERT INTO services (nom, description) OUTPUT INSERTED.id VALUES (?, ?)",
            (service.nom.strip(), service.description.strip())
        )
        new_id = cursor.fetchone()[0]
        self.db.connection.commit()
        self.db.log_action("services", "INSERT", new_id, f"Création du service '{service.nom}'")
        return new_id

    def update(self, service: Service):
        """Met à jour un service existant."""
        self.db.execute(
            "UPDATE services SET nom = ?, description = ?, actif = ? WHERE id = ?",
            (service.nom.strip(), service.description.strip(), service.actif, service.id)
        )
        self.db.connection.commit()
        self.db.log_action("services", "UPDATE", service.id, f"Modification du service '{service.nom}'")

    def delete(self, service_id: int):
        """Supprime un service."""
        service = self.get_by_id(service_id)
        nom = service.nom if service else "?"
        self.db.execute("DELETE FROM services WHERE id = ?", (service_id,))
        self.db.connection.commit()
        self.db.log_action("services", "DELETE", service_id, f"Suppression du service '{nom}'")

    def count_equipements(self, service_id: int) -> int:
        """Compte les équipements associés à un service."""
        row = self.db.fetch_one("SELECT COUNT(*) FROM equipements WHERE service_id = ?", (service_id,))
        return row[0] if row else 0
