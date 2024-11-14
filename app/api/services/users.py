from typing import Optional, List
from uuid import uuid4

import jwt
from fastapi import HTTPException
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

import models
from models import get_db
from schemas.users import User, UserCreate, UserInDB

# Fonction pour créer un nouvel utilisateur dans la base de données
def create_user(db: Session, user: UserCreate) -> UserInDB:
    # Vérifie si un utilisateur avec le même nom d'utilisateur existe déjà dans la base de données
    record = db.query(models.User).filter(models.User.username == user.username).first()
    if record:
        # Si l'utilisateur existe déjà, on renvoie une erreur 409 (conflit)
        raise HTTPException(status_code=409, detail="Username already taken")

    # Création d'un nouvel utilisateur avec un identifiant unique généré et les informations fournies
    db_user = models.User(
        id=str(uuid4()), username=user.username, password=user.password
    )
    # Ajout de l'utilisateur dans la session de la base de données
    db.add(db_user)
    # Validation de la transaction
    db.commit()
    # Rafraîchissement de l'objet pour récupérer les données mises à jour (comme l'ID généré)
    db.refresh(db_user)

    # Retourne l'utilisateur créé sous forme d'instance UserInDB (modèle de données utilisé dans les réponses)
    return UserInDB.from_orm(db_user)


# Fonction pour récupérer tous les utilisateurs de la base de données
def get_all_users(db: Session) -> List[models.User]:
    # Récupère tous les utilisateurs sans filtrage particulier
    return db.query(models.User).filter().all()


# Fonction pour récupérer un utilisateur en fonction de son ID
def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    # Recherche un utilisateur dans la base de données avec l'ID spécifié
    return db.query(models.User).filter(models.User.id == user_id).first()
