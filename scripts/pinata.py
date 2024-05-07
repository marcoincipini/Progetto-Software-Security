"""Modulo che implementa una serie di funzionalità per utilizzare Pinata"""
import os
import requests
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

def get_file_from_pinata(ipfs_hash):
    """Modulo che implementa una serie di funzionalità per prendere file da Pinata"""
    url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"

    # salvo in una variabile la chiave API necessaria per la richiesta a Pinata
    jwt_token = os.getenv('PINATA_JWT_TOKEN')

    headers = {'Authorization': f'Bearer {jwt_token}'}

    try:

        #invia una richiesta GET all'URL specificato,
        #inclusi gli header forniti, e memorizza
        #la risposta nella variabile response.
        #La risposta conterrà i dati restituiti dal server
        #al quale è stata inviata la richiesta GET.

        response = requests.get(url, headers=headers, timeout = 10)
        response.raise_for_status()  # Solleva un'eccezione se la richiesta HTTP non ha successo

        # Parse della risposta json
        file_data = response.json()
        return file_data
    except requests.exceptions.RequestException as e:
        # controllo su eventuali errori della richiesta http
        print("Errore durante la richiesta HTTP:", e)
        return None

def upload_to_pinata(filepath):
    """Modulo che implementa una serie di funzionalità per caricare file su Pinata"""
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    # salvo in una variabile la chiave API necessaria per la richiesta a Pinata
    jwt_token = os.getenv('PINATA_JWT_TOKEN')

    headers = {'Authorization': f'Bearer {jwt_token}'}

    with open(filepath, 'rb') as file:

        # Invia una richiesta POST all'URL specificato,
        # inclusi i dati del file e gli header forniti, e memorizza
        # la risposta nella variabile response.
        # La risposta conterrà i dati restituiti dal server
        # al quale è stata inviata la richiesta POST.

        response = requests.post(url, files={'file': file}, headers=headers, timeout = 10)
        response_json = response.json() # restituisce il json associato al file caricato su Pinata
        print(response_json)
        # Estrai l'hash del file caricato dal JSON di risposta
        ipfs_hash = response_json.get('IpfsHash', None)
        print(ipfs_hash)
        return ipfs_hash  # Restituisci l'hash del file caricato

def upload_files_in_folder(folder_path):
    """
    Modulo che implementa una serie di funzionalità 
    per caricare uno per uno tutti i file da una cartella a Pinata
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            print(f"Uploading file: {file_path}")
            response = upload_to_pinata(file_path)
            print(f"IPFS Hash: {response['IpfsHash']}")
            print()
