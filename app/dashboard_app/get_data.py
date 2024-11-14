import pandas as pd
import requests
import aiohttp
import asyncio

# Variable globale pour stocker les données mises en cache
cached_data = None

# Fonction asynchrone pour récupérer les données
async def fetch_data():
    global cached_data
    if cached_data is None:  # Si les données ne sont pas encore récupérées
        # Données utilisateur pour la création de l'utilisateur et l'obtention du token
        user_data = {"firstName": "get_data", "password": "get_data_password"}

        # Envoi de la requête POST pour créer un nouvel utilisateur
        create_user_response = requests.post("http://api:5000/users/", json=user_data)
        if create_user_response.status_code == 201:
            print(create_user_response)  # Si la création réussit, on affiche la réponse

        # Envoi de la requête POST pour obtenir un token d'accès
        token_response = requests.post("http://api:5000/token/", json=user_data)
        if token_response.status_code == 200:
            token = token_response.json()["access_token"]  # Extraction du token d'accès
            header = {"Authorization": f"Bearer {token}"}  # Préparation des headers avec le token
        else:
            print("Erreur lors de la récupération du token:", token_response.json())  # Gestion de l'erreur si le token n'est pas récupéré

        # Requête asynchrone pour récupérer les données d'attaques
        async with aiohttp.ClientSession() as session:
            async with session.get("http://api:5000/attacks/", headers=header) as response:
                if response.status == 200:
                    json_data = await response.json()  # Conversion de la réponse en JSON
                    cached_data = pd.DataFrame(json_data)  # Stockage des données dans la variable globale sous forme de DataFrame
                else:
                    cached_data = None  # Si la requête échoue, on réinitialise les données

    return cached_data  # Retourner les données récupérées ou None si la requête échoue

# Fonction pour obtenir les données en appelant la fonction asynchrone fetch_data
def get_data():
    data = asyncio.run(fetch_data())  # Exécution de la fonction asynchrone avec asyncio.run
    return data  # Retourne les données récupérées
