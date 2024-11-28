from fastapi import FastAPI, HTTPException, status, File, UploadFile, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder

import pandas as pd
import requests

from models.authentification import verify_autorization_header, _encode_jwt
from models.users import User
from models.attack import Attack
import models
from models.database import engine
from models.db import get_db
from schemas.users import UserCreate, UserInDB
from schemas.attacks import AttackCreate, AttackInDB, AttackUpdate

security = HTTPBearer()  # Définit la sécurité HTTP pour l'authentification par token
router = APIRouter()

# Initialisation de l'application FastAPI
app = FastAPI(
    title="API vers les attaques de requin dans le monde",  # Titre de l'API
    description="API créée afin de d'importer ou de récupérer des données sur les attaques de requin dans le monde",  # Description de l'API
    version="1.0",  # Version de l'API
)

# Configuration des origines autorisées pour CORS
origins = [
    "http://localhost:80",  # Ajoute localhost:80 comme origine autorisée
    "http://localhost:9001",  # Ajoute localhost:9001 comme origine autorisée
    "http://localhost:5000",  # Ajoute localhost:5000 comme origine autorisée
    "http://localhost:8050"  # Ajoute localhost:8050 comme origine autorisée
]

# Ajout du middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Origines autorisées
    allow_credentials=True,
    allow_methods=["*"],  # Méthodes autorisées (toutes les méthodes HTTP)
    allow_headers=["*"],  # En-têtes autorisés (tous les en-têtes)
)

# Événement de démarrage : crée les tables de la base de données
@app.on_event("startup")
async def startup_event():
    models.Base.metadata.create_all(bind=engine)

# Route de base (racine) pour tester si l'API fonctionne
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API des attaques de requin"}

# Route pour obtenir un token JWT en fonction des informations d'utilisateur
@app.post("/token/", description="Génère un token JWT pour un utilisateur en fonction de ses informations d'authentification.")
def token(user: UserCreate, db: Session = Depends(get_db)):
    user_record = db.query(models.User).filter(models.User.firstName == user.firstName).first()
    if not user_record or user_record.password != user.password:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    token = _encode_jwt(user=user_record)
    return {"access_token": token}

# Route pour créer un nouvel utilisateur
@app.post("/users/", response_model=UserInDB, status_code=status.HTTP_201_CREATED, description="Crée un nouvel utilisateur en fournissant un prénom et un mot de passe.")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.firstName == user.firstName).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="firstName already exists")
    db_user = models.User(firstName=user.firstName, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserInDB.from_orm(db_user)

# Route pour obtenir un utilisateur par son ID
@app.get("/users/{user_id}", dependencies=[Depends(security)], description="Récupère les informations d'un utilisateur par son ID.")
def get_user(user_id: int, db: Session = Depends(get_db), authorization=Depends(security)):
    auth_header = f"Bearer {authorization.credentials}"
    auth = verify_autorization_header(auth_header)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Route pour mettre à jour un utilisateur
@app.put("/users/{user_id}", dependencies=[Depends(security)], response_model=UserInDB, description="Met à jour les informations d'un utilisateur en fournissant un nouvel identifiant et/ou mot de passe.")
def update_user(user_id: int, updated_user: UserCreate, db: Session = Depends(get_db), authorization=Depends(security)):
    auth_header = f"Bearer {authorization.credentials}"
    auth = verify_autorization_header(auth_header)
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.firstName = updated_user.firstName
    user.password = updated_user.password
    db.commit()
    db.refresh(user)
    return UserInDB.from_orm(user)

# Route pour supprimer un utilisateur
@app.delete("/users/{user_id}", dependencies=[Depends(security)], status_code=status.HTTP_204_NO_CONTENT, description="Supprime un utilisateur en fonction de son ID.")
def delete_user(user_id: int, db: Session = Depends(get_db), authorization=Depends(security)):
    auth_header = f"Bearer {authorization.credentials}"
    auth = verify_autorization_header(auth_header)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}

# Route pour obtenir tous les utilisateurs
@app.get("/users/", dependencies=[Depends(security)], description="Retourne la liste de tous les utilisateurs.")
def get_all_users(db: Session = Depends(get_db), authorization=Depends(security)):
    auth_header = f"Bearer {authorization.credentials}"
    auth = verify_autorization_header(auth_header)
    users = db.query(User).all()
    return users

# Route pour obtenir une attaque par son ID
@app.get("/attacks/{attack_id}", description="Récupère les informations d'une attaque spécifique par son ID.")
def get_attack(attack_id: int, db: Session = Depends(get_db), authorization=Depends(security)):
    auth_header = f"Bearer {authorization.credentials}"
    auth = verify_autorization_header(auth_header)
    attack = db.query(Attack).filter(Attack.id == attack_id).first()
    if not attack:
        raise HTTPException(status_code=404, detail="Attack not found")
    return attack

# Route pour créer une nouvelle attaque
@app.post("/attacks/", dependencies=[Depends(security)], response_model=AttackInDB, status_code=status.HTTP_201_CREATED, description="Crée une nouvelle attaque en fournissant toutes les informations nécessaires.")
def create_attack(attack: AttackCreate, db: Session = Depends(get_db), authorization=Depends(security)):
    auth_header = f"Bearer {authorization.credentials}"
    auth = verify_autorization_header(auth_header)
    db_attack = models.Attack(**attack.dict())
    db.add(db_attack)
    db.commit()
    db.refresh(db_attack)
    return AttackInDB.from_orm(db_attack)

# Route pour mettre à jour une attaque
@app.put("/attacks/{attack_id}", dependencies=[Depends(security)], response_model=AttackInDB, description="Met à jour les informations d'une attaque existante.")
def update_attack(attack_id: int, updated_attack: AttackUpdate, db: Session = Depends(get_db), authorization=Depends(security)):
    auth_header = f"Bearer {authorization.credentials}"
    auth = verify_autorization_header(auth_header)
    attack = db.query(models.Attack).filter(models.Attack.id == attack_id).first()
    if not attack:
        raise HTTPException(status_code=404, detail="Attack not found")
    for key, value in updated_attack.dict(exclude_unset=True).items():
        setattr(attack, key, value)
    db.commit()
    db.refresh(attack)
    return AttackInDB.from_orm(attack)

# Route pour supprimer une attaque
@app.delete("/attacks/{attack_id}", dependencies=[Depends(security)], status_code=status.HTTP_204_NO_CONTENT, description="Supprime une attaque spécifique par son ID.")
def delete_attack(attack_id: int, db: Session = Depends(get_db), authorization=Depends(security)):
    auth_header = f"Bearer {authorization.credentials}"
    auth = verify_autorization_header(auth_header)
    attack = db.query(Attack).filter(models.Attack.id == attack_id).first()
    if not attack:
        raise HTTPException(status_code=404, detail="Attack not found")
    db.delete(attack)
    db.commit()
    return {"detail": "Attack deleted"}

# Route pour importer toutes les attaques depuis un fichier CSV
@app.post("/attacks/post_all_attacks/", dependencies=[Depends(security)])
async def post_all_attacks(db: Session = Depends(get_db), authorization=Depends(security)):
    import csv
    file_path = "/app/models/data/attacks.csv"

    # Vérification du token d'authentification
    auth_header = f"Bearer {authorization.credentials}"
    auth = verify_autorization_header(auth_header)

    with open(file_path, newline='', encoding='latin-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                attack_data = AttackCreate(
                    type=row.get("Type"),
                    location=row.get("Location"),
                    year= row.get("Year"),
                    country=row.get("Country"),
                    area=row.get("Area"),
                    activity=row.get("Activity"),
                    name=row.get("Name"),
                    sex=row.get("Sex "),
                    age=int(row["Age"]) if row["Age"].isdigit() else None,
                    injury=row.get("Injury"),
                    fatal=row.get("Fatal (Y/N)"),
                    time=row.get("Time"),
                    species=row.get("Species "),  # Note: Vérifie l'espace dans le nom de la colonne
                    investigator=row.get("Investigator or Source"),
                    pdf=row.get("pdf"),
                    href_formula=row.get("href formula"),
                    href=row.get("href"),
                    caseNumber=row.get("Case Number"),
                    original_order=row.get("original order")
                ) 
                
                # Création de l'instance Attack
                db_attack = Attack(**attack_data.dict())
                db.add(db_attack)

            db.commit()
    return {"message": "All attacks have been posted"}

# Route pour obtenir toutes les attaques
@app.get("/attacks/", dependencies=[Depends(security)], description="Retourne la liste complète des attaques dans la base de données.")
def get_all_attacks(db: Session = Depends(get_db), authorization=Depends(security)):
    auth_header = f"Bearer {authorization.credentials}"
    auth = verify_autorization_header(auth_header)
    attacks = db.query(Attack).all()
    return attacks