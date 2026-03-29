"""
Modèles de données (Data classes).
Représentent les entités métier de l'application.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass
class Service:
    """Modèle représentant un service."""
    id: Optional[int] = None
    nom: str = ""
    description: str = ""
    date_creation: Optional[datetime] = None
    actif: bool = True


@dataclass
class SousService:
    """Modèle représentant un sous-service."""
    id: Optional[int] = None
    nom: str = ""
    service_id: Optional[int] = None
    service_nom: str = ""  # Pour l'affichage
    description: str = ""
    date_creation: Optional[datetime] = None
    actif: bool = True


@dataclass
class Categorie:
    """Modèle représentant une catégorie d'équipement."""
    id: Optional[int] = None
    nom: str = ""


@dataclass
class Equipement:
    """Modèle représentant un équipement (actif)."""
    id: Optional[int] = None
    nom: str = ""
    categorie_id: Optional[int] = None
    categorie_nom: str = ""
    numero_serie: str = ""
    date_achat: Optional[date] = None
    statut: str = "Actif"
    service_id: Optional[int] = None
    service_nom: str = ""
    sous_service_id: Optional[int] = None
    sous_service_nom: str = ""
    notes: str = ""
    date_creation: Optional[datetime] = None
    date_modification: Optional[datetime] = None


@dataclass
class Transfert:
    """Modèle représentant un transfert d'équipement."""
    id: Optional[int] = None
    equipement_id: Optional[int] = None
    equipement_nom: str = ""
    ancien_service_id: Optional[int] = None
    ancien_service_nom: str = ""
    nouveau_service_id: Optional[int] = None
    nouveau_service_nom: str = ""
    ancien_sous_service_id: Optional[int] = None
    nouveau_sous_service_id: Optional[int] = None
    date_transfert: Optional[datetime] = None
    motif: str = ""
