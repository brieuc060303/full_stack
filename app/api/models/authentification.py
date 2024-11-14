import os
import jwt
from fastapi import HTTPException
from .users import User

# Récupération des clés et de l'algorithme de cryptage du JWT depuis les variables d'environnement
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Clé secrète pour signer et vérifier le JWT
JWT_SECRET_ALGORITHM = os.getenv("JWT_SECRET_ALGORITHM")  # Algorithme utilisé pour signer le JWT

# Fonction pour vérifier l'en-tête d'autorisation (Bearer token)
def verify_autorization_header(access_token: str):
    # Si l'élément 'access_token' est manquant ou mal formaté (ne commence pas par 'Bearer ')
    if not access_token or not access_token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No authentification provided.")  # Erreur 401 si pas d'authentification

    try:
        # Extraction du token après "Bearer " dans l'en-tête
        token = access_token.split("Bearer ")[1]
        # Décodage du token en utilisant la clé secrète et l'algorithme spécifiés
        auth = jwt.decode(
            token, JWT_SECRET_KEY, JWT_SECRET_ALGORITHM
        )
    except jwt.InvalidTokenError as err:
        # Si le token est invalide (erreur de décodage)
        raise HTTPException(status_code=401, detail=f"Invalid token.")  # Erreur 401 pour un token invalide

    return auth  # Retourne les informations contenues dans le token

# Fonction pour encoder un JWT à partir des informations d'un utilisateur
def _encode_jwt(user: User) -> str:
    return jwt.encode(
        {
            "user_id": user.id,  # Inclut l'identifiant de l'utilisateur dans le token
        },
        JWT_SECRET_KEY,  # Utilise la clé secrète pour signer le token
        algorithm=JWT_SECRET_ALGORITHM,  # Utilise l'algorithme spécifié
    )

# Fonction pour décoder un JWT et récupérer ses informations
def _decode_jwt(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_SECRET_ALGORITHM])  # Décodage du token avec la clé et l'algorithme
