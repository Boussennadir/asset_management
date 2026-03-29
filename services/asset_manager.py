"""
Gestionnaire des équipements (logique métier).
"""

import logging
from typing import List, Optional, Dict, Any

from database.db_manager import DatabaseManager
from models.models import Equipement

logger = logging.getLogger(__name__)

# Requête de base pour récupérer les équipements avec jointures
_BASE_QUERY = """
    SELECT e.id, e.nom, e.categorie_id, c.nom, e.numero_serie,
           e.date_achat, e.statut, e.service_id, s.nom,
           e.sous_service_id, ISNULL(ss.nom, ''), e.notes,
           e.date_creation, e.date_modification
    FROM equipements e
    JOIN categories c ON e.categorie_id = c.id
    JOIN services s ON e.service_id = s.id
    LEFT JOIN sous_services ss ON e.sous_service_id = ss.id
"""


def _row_to_equipement(r) -> Equipement:
    return Equipement(
        id=r[0], nom=r[1], categorie_id=r[2], categorie_nom=r[3],
        numero_serie=r[4] or "", date_achat=r[5], statut=r[6],
        service_id=r[7], service_nom=r[8],
        sous_service_id=r[9], sous_service_nom=r[10] or "",
        notes=r[11] or "", date_creation=r[12], date_modification=r[13]
    )


class AssetManager:
    """Gère les opérations CRUD sur les équipements."""

    def __init__(self):
        self.db = DatabaseManager()
    
    def generate_code(self, categorie_nom, service_nom, next_id):
        cat = categorie_nom[:3].upper()
        serv = service_nom[:3].upper()
        return f"{cat}-{serv}-{str(next_id).zfill(5)}"
    
    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Equipement]:
        """Récupère les équipements avec filtres optionnels."""
        query = _BASE_QUERY
        conditions = []
        params = []

        if filters:
            if filters.get("service_id"):
                conditions.append("e.service_id = ?")
                params.append(filters["service_id"])
            if filters.get("statut"):
                conditions.append("e.statut = ?")
                params.append(filters["statut"])
            if filters.get("categorie_id"):
                conditions.append("e.categorie_id = ?")
                params.append(filters["categorie_id"])
            if filters.get("recherche"):
                conditions.append("(e.nom LIKE ? OR e.numero_serie LIKE ? OR s.nom LIKE ?)")
                term = f"%{filters['recherche']}%"
                params.extend([term, term, term])

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY e.nom"

        rows = self.db.fetch_all(query, tuple(params))
        return [_row_to_equipement(r) for r in rows]

    def get_by_id(self, eq_id: int) -> Optional[Equipement]:
        row = self.db.fetch_one(_BASE_QUERY + " WHERE e.id = ?", (eq_id,))
        return _row_to_equipement(row) if row else None

    def create(self, eq: Equipement) -> int:
       if eq.numero_serie:
        existing = self.db.fetch_one(
            "SELECT id FROM equipements WHERE numero_serie = ?",
            (eq.numero_serie.strip(),)
        )
        if existing:
            raise ValueError("Ce numéro de série existe déjà !")

        cursor = self.db.execute(
            """INSERT INTO equipements (nom, categorie_id, numero_serie, date_achat, statut,
            service_id, sous_service_id, notes)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (eq.nom.strip(), eq.categorie_id, eq.numero_serie.strip() or None,
            eq.date_achat, eq.statut, eq.service_id,
            eq.sous_service_id if eq.sous_service_id else None, eq.notes.strip())
        )

        new_id = cursor.fetchone()[0]

        cat = self.db.fetch_one(
            "SELECT nom FROM categories WHERE id=?",
            (eq.categorie_id,)
        )[0]

        serv = self.db.fetch_one(
            "SELECT nom FROM services WHERE id=?",
            (eq.service_id,)
        )[0]

        code = self.generate_code(cat, serv, new_id)

        self.db.execute(
            "UPDATE equipements SET code=? WHERE id=?",
            (code, new_id)
        )

        self.db.connection.commit()
        self.db.log_action(
            "equipements",
            "INSERT",
            new_id,
            f"Ajout équipement: {eq.nom}"
        )

        return new_id

    def update(self, eq: Equipement):
        old = self.get_by_id(eq.id)
        if eq.numero_serie:
            existing = self.db.fetch_one(
                "SELECT id FROM equipements WHERE numero_serie = ? AND id != ?",
                (eq.numero_serie.strip(),eq.id)
            )
            if existing:
                raise ValueError("Ce numéro de série existe déjà !")
        self.db.execute(
            """UPDATE equipements SET nom=?, categorie_id=?, numero_serie=?, date_achat=?,
               statut=?, service_id=?, sous_service_id=?, notes=?, date_modification=GETDATE()
               WHERE id=?""",
            (eq.nom.strip(), eq.categorie_id, eq.numero_serie.strip() or None,
             eq.date_achat, eq.statut, eq.service_id,
             eq.sous_service_id if eq.sous_service_id else None, eq.notes.strip(), eq.id)
        )
        self.db.connection.commit() 
        
        changes = []
        if old.nom != eq.nom:
            changes.append(f"Nom: {old.nom} → {eq.nom}")

        if old.numero_serie != eq.numero_serie:
            changes.append(f"S/N: {old.numero_serie} → {eq.numero_serie}")

        if old.date_achat != eq.date_achat:
            changes.append(f"Date: {old.date_achat} → {eq.date_achat}")

        if old.statut != eq.statut:
            changes.append(f"Statut: {old.statut} → {eq.statut}")

        if old.service_id != eq.service_id:
            changes.append(f"Service: {old.service_id} → {eq.service_id}")

        if old.sous_service_id != eq.sous_service_id:
            changes.append(f"Sous-service: {old.sous_service_id} → {eq.sous_service_id}")

        if old.notes != eq.notes:
            changes.append("Notes modifiées")

        details = " | ".join(changes) if changes else "Aucune modification"

        self.db.log_action(
            "equipements",
            "UPDATE",
            eq.id,
            details
        )

    def delete(self, eq_id: int):
        eq = self.get_by_id(eq_id)
        nom = eq.nom if eq else "?"
        self.db.execute("DELETE FROM equipements WHERE id = ?", (eq_id,))
        self.db.connection.commit() 
        self.db.log_action(
            "equipements",
            "DELETE",
            eq_id,
            f"Suppression: {eq.nom}"
        )

    def transfer(self, eq_id: int, new_service_id: int, new_ss_id: Optional[int], motif: str = ""):
        """Transfère un équipement vers un autre service/sous-service."""

        old = self.get_by_id(eq_id)
        if not old:
            raise ValueError("Équipement introuvable.")

        new_service = self.db.fetch_one(
            "SELECT nom FROM services WHERE id=?",
            (new_service_id,)
        )[0]

        self.db.execute(
            """INSERT INTO transferts (equipement_id, ancien_service_id, nouveau_service_id,
            ancien_sous_service_id, nouveau_sous_service_id, motif)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (eq_id, old.service_id, new_service_id,
            old.sous_service_id, new_ss_id, motif.strip())
        )

        self.db.execute(
            "UPDATE equipements SET service_id=?, sous_service_id=?, date_modification=GETDATE() WHERE id=?",
            (new_service_id, new_ss_id, eq_id)
        )

        self.db.connection.commit()

        self.db.log_action(
            "equipements",
            "TRANSFER",
            eq_id,
            f"Service: {old.service_nom} → {new_service}"
        )

    def get_stats(self) -> Dict[str, int]:
        """Statistiques pour le tableau de bord."""
        stats = {}
        row = self.db.fetch_one("SELECT COUNT(*) FROM equipements")
        stats["total"] = row[0] if row else 0

        for statut in ["Actif", "Maintenance", "En panne"]:
            row = self.db.fetch_one("SELECT COUNT(*) FROM equipements WHERE statut = ?", (statut,))
            stats[statut.lower().replace(" ", "_")] = row[0] if row else 0

        row = self.db.fetch_one("SELECT COUNT(*) FROM services")
        stats["services"] = row[0] if row else 0

        row = self.db.fetch_one("SELECT COUNT(*) FROM sous_services")
        stats["sous_services"] = row[0] if row else 0

        return stats
