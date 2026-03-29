-- ============================================
-- Asset Management System - SQL Server Schema
-- ============================================

-- Création de la base de données
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'asset_db')
BEGIN
    CREATE DATABASE asset_db;
END
GO

USE asset_db;
GO

-- ============================================
-- Table: services
-- ============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='services' AND xtype='U')
CREATE TABLE services (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    nom         NVARCHAR(150) NOT NULL UNIQUE,
    description NVARCHAR(500) NULL,
    date_creation DATETIME DEFAULT GETDATE(),
    actif       BIT DEFAULT 1
);
GO

-- ============================================
-- Table: sous_services
-- ============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='sous_services' AND xtype='U')
CREATE TABLE sous_services (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    nom         NVARCHAR(150) NOT NULL,
    service_id  INT NOT NULL,
    description NVARCHAR(500) NULL,
    date_creation DATETIME DEFAULT GETDATE(),
    actif       BIT DEFAULT 1,
    CONSTRAINT FK_sous_services_service FOREIGN KEY (service_id)
        REFERENCES services(id) ON DELETE CASCADE,
    CONSTRAINT UQ_sous_service_nom UNIQUE (nom, service_id)
);
GO

-- ============================================
-- Table: categories
-- ============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='categories' AND xtype='U')
CREATE TABLE categories (
    id   INT IDENTITY(1,1) PRIMARY KEY,
    nom  NVARCHAR(100) NOT NULL UNIQUE
);
GO

-- Insertion de catégories par défaut
INSERT INTO categories (nom) VALUES
    (N'Informatique'),
    (N'Mobilier'),
    (N'Électronique'),
    (N'Véhicule'),
    (N'Autre');
GO

-- ============================================
-- Table: equipements (assets)
-- ============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='equipements' AND xtype='U')
CREATE TABLE equipements (
    id              INT IDENTITY(1,1) PRIMARY KEY,
    nom             NVARCHAR(200) NOT NULL,
    categorie_id    INT NOT NULL,
    numero_serie    NVARCHAR(100) NULL UNIQUE,
    date_achat      DATE NULL,
    statut          NVARCHAR(20) NOT NULL DEFAULT 'Actif'
                    CHECK (statut IN ('Actif', 'Maintenance', 'En panne')),
    service_id      INT NOT NULL,
    sous_service_id INT NULL,
    notes           NVARCHAR(1000) NULL,
    date_creation   DATETIME DEFAULT GETDATE(),
    date_modification DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_equipements_categorie FOREIGN KEY (categorie_id)
        REFERENCES categories(id),
    CONSTRAINT FK_equipements_service FOREIGN KEY (service_id)
        REFERENCES services(id),
    CONSTRAINT FK_equipements_sous_service FOREIGN KEY (sous_service_id)
        REFERENCES sous_services(id) ON DELETE SET NULL
);
GO

-- ============================================
-- Table: journal (audit log)
-- ============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='journal' AND xtype='U')
CREATE TABLE journal (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    table_nom   NVARCHAR(50) NOT NULL,
    action      NVARCHAR(20) NOT NULL,  -- INSERT, UPDATE, DELETE, TRANSFER
    enregistrement_id INT NOT NULL,
    details     NVARCHAR(MAX) NULL,
    date_action DATETIME DEFAULT GETDATE()
);
GO

-- ============================================
-- Table: transferts (transfer history)
-- ============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='transferts' AND xtype='U')
CREATE TABLE transferts (
    id                      INT IDENTITY(1,1) PRIMARY KEY,
    equipement_id           INT NOT NULL,
    ancien_service_id       INT NOT NULL,
    nouveau_service_id      INT NOT NULL,
    ancien_sous_service_id  INT NULL,
    nouveau_sous_service_id INT NULL,
    date_transfert          DATETIME DEFAULT GETDATE(),
    motif                   NVARCHAR(500) NULL,
    CONSTRAINT FK_transferts_equipement FOREIGN KEY (equipement_id)
        REFERENCES equipements(id),
    CONSTRAINT FK_transferts_ancien_service FOREIGN KEY (ancien_service_id)
        REFERENCES services(id),
    CONSTRAINT FK_transferts_nouveau_service FOREIGN KEY (nouveau_service_id)
        REFERENCES services(id)
);
GO
