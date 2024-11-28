from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Récupération des informations de connexion à la base de données depuis les variables d'environnement
POSTGRES_USER = os.environ.get("POSTGRES_USER")  # Utilisateur de la base de données
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")  # Mot de passe de la base de données
POSTGRES_DB = os.environ.get("POSTGRES_DB")  # Nom de la base de données

# URL de connexion à la base de données PostgreSQL
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db/{POSTGRES_DB}"

# Création de l'engine SQLAlchemy qui gère la connexion à la base de données
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Création du sessionmaker, utilisé pour gérer les sessions avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

# Base déclarative, utilisée pour la création des modèles ORM
Base = declarative_base()
