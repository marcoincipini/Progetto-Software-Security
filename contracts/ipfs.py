from ipfshttpclient import connect

# Specifica l'indirizzo IP e la porta del container IPFS
ipfs_address = "/ip4/0.0.0.0/tcp/5001"

# Connettiti all'API IPFS
ipfs_client = connect(ipfs_address)

# Esempio di caricamento di un file su IPFS
#file_path = "/path/to/your/file.txt"
#res = ipfs_client.add(file_path)

# Ottieni l'hash del file caricato
#ipfs_hash = res['Hash']
#print("File uploaded to IPFS. IPFS Hash:", ipfs_hash)
