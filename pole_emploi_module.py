import os
import requests
import streamlit as st


class JobOffersModule:
    def __init__(self):
        self.url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.data = {
            "grant_type": "client_credentials",
            "client_id": st.secrets["client_id"],
            "client_secret": st.secrets["client_secret"],
            "scope": "api_offresdemploiv2 o2dsoffre",
        }
        self.access_token = self.get_access_token()


    def get_access_token(self):
        response = requests.post(self.url, headers=self.headers, data=self.data)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            raise Exception(f"Error getting access token: {response.text}")

    def fetch_job_offers(self, rome, region):
        URL = f"https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search?codeROME={rome}&&region={region}"

        payload = {}
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        job_offers = []

        try:
            for start in range(0, 3000, 100):
                params = {"range": f"{start}-{start+99}", "codeROME": rome, "region": region}

                response = requests.get(
                    URL, headers=headers, params=params, timeout=1
                )

                data = response.json()
                job_offers += data.get("resultats", [])

        except requests.exceptions.RequestException as e:
            print("Error during API request:", e)

        return job_offers

     
# Utilisation du module backend
if __name__ == "__main__":
    module = JobOffersModule()
    rome = input("Code ROME: ")
    region = input("Code Region: ")
    job_offers = module.fetch_job_offers(rome, region)

    for offer in job_offers:
        offer_id = offer.get("id", "")
        company_name = offer["entreprise"].get("nom", "")
        appellation = offer.get("appellationlibelle", "")
        location = offer["lieuTravail"].get("libelle", "")
        contract_type = offer.get("typeContrat", "")
        number_of_positions = offer.get("nombrePostes", "")

        # Créez ici votre objet ou effectuez les opérations souhaitées avec les données.

    print("Job offers have been fetched and processed.")
