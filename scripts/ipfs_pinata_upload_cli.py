import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def upload_to_pinata(filepath, jwt_token):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {'Authorization': f'Bearer {jwt_token}'}

    with open(filepath, 'rb') as file:
        response = requests.post(url, files={'file': file}, headers=headers)
        return response.json()

def upload_files_in_folder(folder_path, jwt_token):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            print(f"Uploading file: {file_path}")
            response = upload_to_pinata(file_path, jwt_token)
            print(f"IPFS Hash: {response['IpfsHash']}")
            print()

def main():
    PINATA_JWT_TOKEN = os.getenv('PINATA_JWT_TOKEN')

    
    while True:
        # Ask user for input
        user_input = input("Enter 0 to esc or folder path or absolute file path: ")

        # Check if input is "0" to exit
        if user_input == '0':
            print("Exiting...")
            break  # Exit the loop

        # Check if input is a folder or file
        if os.path.isdir(user_input):
            upload_files_in_folder(user_input, PINATA_JWT_TOKEN)
        elif os.path.isfile(user_input):
            print(f"Uploading file: {user_input}")
            response = upload_to_pinata(user_input, PINATA_JWT_TOKEN)
            print(f"IPFS Hash: {response['IpfsHash']}")  
        else:
            print("Invalid input. Please enter a valid folder path or file path.")

if __name__ == "__main__":
    main()
