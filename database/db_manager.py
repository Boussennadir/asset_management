"""
Gestionnaire de base de données.
Gère la connexion à SQL Server via pyodbc et fournit des méthodes utilitaires.
"""

import logging
import pyodbc
from typing import Optional, List, Tuple, Any

from config.settings import Settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Gestionnaire centralisé de la connexion à SQL Server."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection: Optional[pyodbc.Connection] = None
        return cls._instance

    def connect(self) -> bool:
        """Établit la connexion à la base de données."""
        try:
            settings = Settings()
            conn_str = settings.get_connection_string()
            logger.info("Connexion à SQL Server (%s - %s)...", settings.server, settings.database)
            self._connection = pyodbc.connect(conn_str, timeout=10)
            self._connection.autocommit = False
            logger.info("Connexion établie avec succès.")
            return True
        except pyodbc.Error as e:
            logger.error("Erreur de connexion à la base de données: %s", e)
            self._connection = None
            return False

    def disconnect(self):
        """Ferme la connexion."""
        if self._connection:
            try:
                self._connection.close()
                logger.info("Connexion fermée.")
            except pyodbc.Error as e:
                logger.error("Erreur lors de la fermeture: %s", e)
            finally:
                self._connection = None

    @property
    def connection(self) -> Optional[pyodbc.Connection]:
        return self._connection

    @property
    def is_connected(self) -> bool:
        if self._connection is None:
            return False
        try:
            self._connection.cursor().execute("SELECT 1")
            return True
        except pyodbc.Error:
            return False

    def execute(self, query: str, params: tuple = ()) -> Optional[pyodbc.Cursor]:
        """Exécute une requête SQL (INSERT, UPDATE, DELETE)."""
        if not self.is_connected:
            if not self.connect():
                raise ConnectionError("Impossible de se connecter à la base de données.")
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)

          
            return cursor

        except pyodbc.Error as e:
            self._connection.rollback()
            logger.error("Erreur SQL: %s\nRequête: %s\nParamètres: %s", e, query, params)
            raise
    
    def fetch_all(self, query: str, params: tuple = ()) -> List[Tuple[Any, ...]]:
        """Exécute une requête SELECT et retourne toutes les lignes."""
        if not self.is_connected:
            if not self.connect():
                raise ConnectionError("Impossible de se connecter à la base de données.")
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except pyodbc.Error as e:
            logger.error("Erreur SQL (fetch): %s", e)
            raise

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Tuple[Any, ...]]:
        """Exécute une requête SELECT et retourne une seule ligne."""
        if not self.is_connected:
            if not self.connect():
                raise ConnectionError("Impossible de se connecter à la base de données.")
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        except pyodbc.Error as e:
            logger.error("Erreur SQL (fetch_one): %s", e)
            raise

    def log_action(self, table: str, action: str, record_id: int, details: str = "", user: str = "system"):
        """Enregistre une action dans le journal d'audit."""
        try:
            cursor = self.execute(
                """INSERT INTO journal (table_nom, action, enregistrement_id, details)
                VALUES (?, ?, ?, ?)""",
                (table, action, record_id, details)
            )

            self.connection.commit()

        except Exception as e:
            logger.warning("Impossible d'écrire dans le journal: %s", e)