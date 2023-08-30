import os
import requests
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

class JobOffersModule:
    def __init__(self):
        self.url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.data = {
            "grant_type": "client_credentials",
            "client_id": os.environ["client_id"],
            "client_secret": os.environ["client_secret"],
            "scope": "api_labonneboitev1",
        }
        self.access_token = self.get_access_token()

    def get_access_token(self):
        response = requests.post(self.url, headers=self.headers, data=self.data)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            raise Exception(f"Error getting access token: {response.text}")

    def fetch_job_offers(self):
        URL = f"https://api.pole-emploi.io/partenaire/labonneboite/v1/company/?distance=30&latitude=49.119146&longitude=6.17602"

        payload = {}
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        response = requests.get(URL, headers=headers, params=payload)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching job offers: {response.text}")

# Utilisation du module backend
if __name__ == "__main__":
    module = JobOffersModule()
    job_offers = module.fetch_job_offers()

    # Affichage de la réponse en JSON
    print(job_offers)

    # Écrire les données dans un fichier JSON
    with open("job_offers.json", "w") as json_file:
        json.dump(job_offers, json_file, indent=4)

    print("Les offres d'emploi ont été récupérées, traitées et sauvegardées dans job_offers.json.")
