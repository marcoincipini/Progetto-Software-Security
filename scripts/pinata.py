#from brownie import GestioneADI, accounts, Contract
import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def get_file_from_pinata(ipfs_hash):
    url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
    
    jwt_token = os.getenv('PINATA_JWT_TOKEN') # salvo in una variabile la chiave API necessaria per la richiesta a Pinata

    headers = {'Authorization': f'Bearer {jwt_token}'}
    
    try:
        """
        invia una richiesta GET all'URL specificato, inclusi gli header forniti, e memorizza la risposta nella variabile response. 
        La risposta conterrà i dati restituiti dal server al quale è stata inviata la richiesta GET.
        """
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Solleva un'eccezione se la richiesta HTTP non ha successo
        
        # Parse della risposta json
        file_data = response.json()
        print(file_data[1])
        temp_file_path = f"{'Paziente_Piano_terapeutico'}.json"

        # Scrittura del dizionario nel file JSON temporaneo
        with open(temp_file_path, 'w') as temp_file:
            json.dump(file_data, temp_file, indent=4)
        #print(file_data)
        # contenuto del file originale estratto dal file di risposta di pinata
        #original_file_content = file_data["payload"]["blob"]["rawLines"] 
        # conversione della lista di caratteri ottenuta alla riga precedente in una stringa
        #stringa = ''.join(original_file_content) 
        #conversione della stringa ottenuta sopra in una lista di oggetti json
        #json_data = json.loads(file_data)
        #print(json_data)
        #return json_data
    except requests.exceptions.RequestException as e:
        print("Errore durante la richiesta HTTP:", e) # controllo su eventuali errori della richiesta http
        return None

def upload_to_pinata(filepath):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    
    jwt_token = os.getenv('PINATA_JWT_TOKEN') # salvo in una variabile la chiave API necessaria per la richiesta a Pinata

    headers = {'Authorization': f'Bearer {jwt_token}'}

    with open(filepath, 'rb') as file:
        """
         Invia una richiesta POST all'URL specificato, inclusi i dati del file e gli header forniti, e memorizza 
         la risposta nella variabile response. 
         La risposta conterrà i dati restituiti dal server al quale è stata inviata la richiesta POST.
        """
        response = requests.post(url, files={'file': file}, headers=headers)
        response_json = response.json() # restituisce il json associato al file caricato su Pinata
        print(response_json)
        # Estrai l'hash del file caricato dal JSON di risposta
        ipfs_hash = response_json.get('IpfsHash', None)
        print(ipfs_hash)
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

