import sys
import requests
import os
from dotenv import load_dotenv
import pprint

# Specify the directory where you want to save the file
save_directory = "/Users/simonegiano/Desktop/ipfsstaging"

# Load environment variables
load_dotenv()

def get_file_from_pinata(jwt_token, ipfs_hash):
    url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
    headers = {'Authorization': f'Bearer {jwt_token}'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Solleva un'eccezione se la richiesta HTTP non ha successo
        return response.content  # Return the file content
    except requests.exceptions.RequestException as e:
        print("Errore durante la richiesta HTTP:", e)
        return None

def main():
    # Check if IPFS hash argument is provided
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <IPFS_hash>")
        return

    IPFS_HASH = sys.argv[1]  # Get IPFS hash from command line arguments

    PINATA_JWT_TOKEN = os.getenv('PINATA_JWT_TOKEN')

    file_content = get_file_from_pinata(PINATA_JWT_TOKEN, IPFS_HASH)

    # Now you can do something with the file content, e.g., save it to a file in the specified directory
    with open(os.path.join(save_directory, "retrieved_file.txt"), "wb") as file:
        file.write(file_content)


if __name__ == "__main__":
    main()
