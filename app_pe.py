import requests
import csv
import pandas as pd
import os
from dotenv import load_dotenv

url = 'https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=%2Fpartenaire'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}
load_dotenv()

data = {
    'grant_type': 'client_credentials',
    'client_id':os.getenv('client_id'),
    'client_secret': os.getenv('client_secret'),
    'scope': 'api_offresdemploiv2 o2dsoffre'
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    access_token = response.json().get('access_token')
    print('Access Token:', access_token)
    code_rome = input('Code ROME: ')
    url = f"https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search?codeROME={code_rome}"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    try:
        response = requests.get(url, headers=headers, data=payload)
        response.raise_for_status()

        data = response.json()
        csv_file_name = 'job_offers.csv'
        csv_header = ['ID', 'Company Name', 'Appellationlibelle', 'lieuTravail', 'typeContrat', 'Number of Positions']

        with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            csv_writer.writerow(csv_header)

            for start in range(0, 2000, 100):
                params = {
                    'range': f'{start}-{start+99}',
                    'codeROME': code_rome
                }

                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()

                data = response.json()

                for offer in data.get('resultats', []):
                    offer_id = offer.get('id', '')
                    entreprise = offer['entreprise']
                    company_name = entreprise.get('nom', '')
                    appellationlibelle = offer.get('appellationlibelle', '')
                    lieu_travail = offer['lieuTravail']
                    job_location = lieu_travail.get('libelle', '')
                    typeContrat = offer.get('typeContrat', '')
                    nombre_postes = offer.get('nombrePostes', '')
                    
                   
                    csv_writer.writerow([offer_id, company_name, appellationlibelle, job_location, typeContrat, nombre_postes])

            print("CSV file 'job_offers.csv' has been created.")
            df = pd.read_csv('/Users/camille/repo/projet_perso/pole_emploi/job_offers.csv', sep=';')
            print("Number of job offers:", len(df))

    except requests.exceptions.RequestException as e:
        print("Error during API request:", e)
else:
    print('Error:', response.text)
df = pd.read_csv('/Users/camille/repo/projet_perso/pole_emploi/job_offers.csv', sep=';')
#ount groupby entreprises
df_entreprises = df.groupby('Company Name').size().reset_index(name='Count')
df_entreprises_sorted = df_entreprises.sort_values(by='Count', ascending=False)
df_entreprises_sorted.to_csv('/Users/camille/repo/projet_perso/pole_emploi/entreprises.csv', sep=';', index=False)