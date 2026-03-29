# 📊 Asset Management System — Cabinet Fiscal

Système de gestion des actifs (équipements) pour un cabinet fiscal, développé en **PyQt6** avec **Microsoft SQL Server**.

## 📁 Structure du projet

```
asset_management/
├── main.py                     # Point d'entrée
├── config.ini                  # Configuration base de données
├── requirements.txt            # Dépendances Python
├── README.md
├── config/
│   ├── __init__.py
│   └── settings.py             # Lecture config.ini (singleton)
├── database/
│   ├── __init__.py
│   └── db_manager.py           # Connexion SQL Server (singleton)
├── models/
│   ├── __init__.py
│   └── models.py               # Dataclasses (Service, Equipement, etc.)
├── services/
│   ├── __init__.py
│   ├── service_manager.py      # CRUD Services
│   ├── sous_service_manager.py # CRUD Sous-services
│   ├── asset_manager.py        # CRUD Équipements + transferts
│   └── category_manager.py     # CRUD Catégories
├── ui/
│   ├── __init__.py
│   ├── main_window.py          # Fenêtre principale + sidebar
│   ├── dialogs/
│   │   ├── __init__.py
│   │   ├── service_dialog.py
│   │   ├── sous_service_dialog.py
│   │   ├── equipement_dialog.py
│   │   └── transfer_dialog.py
│   └── pages/
│       ├── __init__.py
│       ├── dashboard_page.py
│       ├── services_page.py
│       ├── sous_services_page.py
│       └── equipements_page.py
├── resources/
│   ├── __init__.py
│   └── styles.py               # Feuilles de style QSS
└── sql/
    └── schema.sql              # Script de création de la BDD
```

## 🛠️ Prérequis

1. **Python 3.10+**
2. **Microsoft SQL Server** (Express ou autre édition)
3. **ODBC Driver 17 for SQL Server**
   - Windows : [Télécharger ici](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
   - Linux : `sudo apt install msodbcsql17`

## ⚙️ Installation

```bash
# 1. Installer les dépendances Python
pip install -r requirements.txt

# 2. Créer la base de données
# Exécuter le script sql/schema.sql dans SQL Server Management Studio (SSMS)
# ou via sqlcmd :
sqlcmd -S localhost\SQLEXPRESS -i sql/schema.sql

# 3. Configurer la connexion
# Modifier config.ini selon votre environnement (voir ci-dessous)

# 4. Lancer l'application
python main.py
```

## 🔧 Configuration de la connexion

Le fichier `config.ini` à la racine du projet permet de basculer entre **local** et **production** :

```ini
[database]
mode=local          # Changer en "production" pour le serveur de l'entreprise

[local]
server=localhost\SQLEXPRESS
database=asset_db
trusted_connection=yes

[production]
server=192.168.1.10
database=asset_db
username=sa
password=VotreMotDePasse
```

- **mode=local** : utilise l'authentification Windows (Trusted Connection)
- **mode=production** : utilise un login SQL Server (UID/PWD)

## 🚀 Fonctionnalités

- ✅ Tableau de bord avec statistiques en temps réel
- ✅ Gestion complète des **Services** (CRUD dynamique)
- ✅ Gestion complète des **Sous-services** (liés à un service)
- ✅ Gestion complète des **Équipements** (ajout, modification, suppression)
- ✅ **Recherche et filtres** (par nom, statut, service)
- ✅ **Transfert** d'équipements entre services
- ✅ **Journal d'audit** (traçabilité des modifications)
- ✅ Indicateurs de statut colorés (Actif 🟢, Maintenance 🟠, En panne 🔴)
- ✅ Validation des saisies avec messages en français
- ✅ Interface entièrement en **français**
- ✅ Architecture MVC modulaire et extensible

## 📝 Licence

Usage interne — Cabinet fiscal.
