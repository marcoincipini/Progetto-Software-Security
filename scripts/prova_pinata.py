from brownie import GestioneADI, accounts, Contract
import json
import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

"""
modificare l'input per avere solamente l'hash, il token jwt viene gestito all'interno/nella funzione. in output devo avere il
json del file che viene poi parsato per ottenere il file originale e in output viene mandato quello 
"""
def get_file_from_pinata(ipfs_hash):
    url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
    headers = {'Authorization': f'Bearer {jwt_token}'}
    
    jwt_token = os.getenv('PINATA_JWT_TOKEN') # salvo in una variabile la chiave API necessaria per la richiesta a Pinata

    try:
        """
        Invia una richiesta GET all'URL specificato, inclusi gli header forniti, e memorizza 
        la risposta nella variabile response. 
        La risposta conterrà i dati restituiti dal server al quale è stata inviata la richiesta GET.
        """
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Solleva un'eccezione se la richiesta HTTP non ha successo
        
        # Parse the JSON response
        file_data = response.json()
        
        # estrazione del file originale dal json ottenuto
        original_file_content = file_data['content']
        
        return original_file_content  # restituisce il contenuto originale del file
    except requests.exceptions.RequestException as e:
        print("Errore durante la richiesta HTTP:", e) # controllo su eventuali errori della richiesta http
        return None

""" 
modificare l'output per ritornare l'hash del file caricato, magari prendendolo dal json
modificare l'input per avere solamente il filepath, il token jwt viene gestito all'interno/nella funzione
mettere una funzione ausiliaria che vada a prendere un file json in input, per ogni paziente e terapia associata vada a 
creare un file singolo, (nella cartella di lavoro automaticamente) con il nome indicato e caricando il file su pinata e 
fornendo in output l'hash di ogni file caricato   
"""
def upload_to_pinata(filepath):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {'Authorization': f'Bearer {jwt_token}'}

    jwt_token = os.getenv('PINATA_JWT_TOKEN') # salvo in una variabile la chiave API necessaria per la richiesta a Pinata

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


"""
funzione che serve per convertire un file .csv che ha come nome di ogni foglio Paziente e Piano terapeutico e li 
converte in dizionari python per fare in modo da usarli nella funzione di caricamento di file json
"""
def csv_to_json(csv_filename):
    # Carica il file CSV in un DataFrame
    df_paziente = pd.read_csv(csv_filename, sheet_name='Paziente')
    df_terapeutico = pd.read_csv(csv_filename, sheet_name='Piano terapeutico')

    # converte ciascun DataFrame in un dizionario in cui le chiavi sono i nomi delle colonne e i valori sono le righe.
    paziente_dict = df_paziente.to_dict(orient='records')
    terapeutico_dict = df_terapeutico.to_dict(orient='records')

    # Crea il dizionario finale, ottenutio inserendo i dizionari all'interno di un dizionario più grande con le chiavi "Paziente" e "Piano_terapeutico".
    data = {
        'Paziente': paziente_dict,
        'Piano_terapeutico': terapeutico_dict
    }

    """
    Il file JSON verrà salvato nella cartella corrente con il nome specificato. 
    os.getcwd() restituisce il percorso della cartella corrente, 
    os.path.join() unisce il percorso della cartella corrente con il nome del file JSON per ottenere il percorso completo.
    """
    json_filename =  os.path.join(os.getcwd(), 'output.json')

    # Salva i dati nel file JSON
    with open(json_filename, 'w') as json_file:
        # tre argomenti: dati da salvare, file in cui salvare i dati e, opzionale, indent che controlla l'indentazione nel file JSON per renderlo più leggibile.
        json.dump(data, json_file, indent=4) 

def json_upload_file(json_file_upload):
    hashes = []

    for item in json_file_upload:

        # Generazione del percorso del file temporaneo nella cartella corrente
        temp_file_path = f"{item['Paziente']}_{item['Piano_terapeutico']}.json"

        # Scrittura del dizionario nel file JSON temporaneo
        with open(temp_file_path, 'w') as temp_file:
            json.dump(item, temp_file, indent=4)

        # Caricamento del file su Pinata e ottenimento dell'hash
        ipfs_hash = upload_to_pinata(temp_file_path)

        # Aggiunta dell'hash alla lista
        hashes.append(ipfs_hash)

        # Rimozione del file temporaneo
        os.remove(temp_file_path)

    return hashes          

t=GestioneADI.deploy(accounts[0],{'from':accounts[0]}) #caricando il contratto sulla blockchain
t.setTerapia(accounts[1],10,10) #chiamo la funzione del contratto solidity
