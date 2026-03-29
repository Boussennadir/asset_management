"""
Gestionnaire de configuration.
Lit le fichier config.ini pour déterminer les paramètres de connexion à la base de données.
"""

import configparser
import os


class Settings:
    """Classe de gestion des paramètres de l'application."""

    _instance = None
    CONFIG_FILE = "config.ini"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    def __init__(self):
        if not self._loaded:
            self._config = configparser.ConfigParser()
            self._load_config()
            self._loaded = True

    def _load_config(self):
        """Charge le fichier de configuration."""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), self.CONFIG_FILE)
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Le fichier de configuration '{config_path}' est introuvable.\n"
                "Veuillez créer un fichier config.ini à la racine du projet."
            )
        self._config.read(config_path, encoding="utf-8")

    @property
    def mode(self) -> str:
        """Retourne le mode actuel (local ou production)."""
        return self._config.get("database", "mode", fallback="local")

    @property
    def server(self) -> str:
        return self._config.get(self.mode, "server")

    @property
    def database(self) -> str:
        return self._config.get(self.mode, "database")

    @property
    def trusted_connection(self) -> bool:
        return self._config.get(self.mode, "trusted_connection", fallback="no").lower() == "yes"

    @property
    def username(self) -> str:
        return self._config.get(self.mode, "username", fallback="")

    @property
    def password(self) -> str:
        return self._config.get(self.mode, "password", fallback="")

    def get_connection_string(self) -> str:
        """Construit la chaîne de connexion pyodbc dynamiquement."""
        driver = "{ODBC Driver 17 for SQL Server}"
        if self.trusted_connection:
            return (
                f"DRIVER={driver};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"Trusted_Connection=yes;"
            )
        else:
            return (
                f"DRIVER={driver};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password};"
            )

    def reload(self):
        """Recharge la configuration."""
        self._loaded = False
        self.__init__()
