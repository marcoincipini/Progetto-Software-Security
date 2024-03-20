#from brownie import GestioneADI, accounts, Contract
import sys
import requests
import os
from dotenv import load_dotenv
#import pprint
load_dotenv()

def get_file_from_pinata(ipfs_hash):
    url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
    headers = {'Authorization': f'Bearer {jwt_token}'}
    
    jwt_token = os.getenv('PINATA_JWT_TOKEN') # salvo in una variabile la chiave API necessaria per la richiesta a Pinata

    try:
        """
        invia una richiesta GET all'URL specificato, inclusi gli header forniti, e memorizza la risposta nella variabile response. 
        La risposta conterrà i dati restituiti dal server al quale è stata inviata la richiesta GET.
        """
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Solleva un'eccezione se la richiesta HTTP non ha successo
        
        # Parse the JSON response
        file_data = response.json()
        
        # estrazione del file originale dal json ottenuto, si può mettere qualsiasi cosa
        original_file_content = file_data['content']
        
        return original_file_content  # restituisce il contenuto originale del file
    except requests.exceptions.RequestException as e:
        print("Errore durante la richiesta HTTP:", e) # controllo su eventuali errori della richiesta http
        return None

def upload_to_pinata(filepath):
    jwt_token = os.getenv('PINATA_JWT_TOKEN') # salvo in una variabile la chiave API necessaria per la richiesta a Pinata

    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {'Authorization': f'Bearer {jwt_token}'}

    with open(filepath, 'rb') as file:
        """
         Invia una richiesta POST all'URL specificato, inclusi i dati del file e gli header forniti, e memorizza 
         la risposta nella variabile response. 
         La risposta conterrà i dati restituiti dal server al quale è stata inviata la richiesta POST.
        """
        response = requests.post(url, files={'file': file}, headers=headers)
        response_json = response.json() # restituisce il json associato al file caricato su Pinata

        # Estrai l'hash del file caricato dal JSON di risposta
        ipfs_hash = response_json.get('IpfsHash', None)

        return ipfs_hash  # Restituisci l'hash del file caricato

"""
Questa funzione prende in input una cartella contentente diversi file e li carica uno per uno su Pinata, tramite chiamate a 
funzione di upload_to_pinata.
"""
def upload_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            print(f"Uploading file: {file_path}")
            response = upload_to_pinata(file_path)
            print(f"IPFS Hash: {response['IpfsHash']}")
            print()