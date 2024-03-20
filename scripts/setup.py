from brownie import accounts, network, Contract, GestioneADI
import json
import pinata

# Devo sempre definire un metodo main
# Il setup serve a sviluppare ul contratto da utilizzare ed inserire i dati iniziali.
def main():
    contratto=GestioneADI.deploy(accounts[0],{'from':accounts[0]})
    #contratto.setPaziente(accounts[1],10,10)
    
    # Devo associare gli account ai vari ruoli
    with open('scripts/pazienti.json','r') as file:
        pazienti = json.load(file)
    
    for item in pazienti:
        contratto.setPaziente(accounts[item['ID']],item['Latitudine'],item['Longitudine'],{'from':accounts[0]})
    for item in range(6,8):
        contratto.setMedico(accounts[item],{'from':accounts[0]})
    for item in range(8,10):
        contratto.setOperatore(accounts[item],{'from':accounts[0]})

    # Istanziare un set di dati di prova per ogni struttura
    with open('scripts/terapie.json','r') as file:
        terapie = json.load(file)
    for i in range(1,6):
        dati= list(filter(lambda x:x["IDPaziente"]==i,terapie))
        with open('temp.json','w') as file:
            json.dump(dati,file)
        try:
            hash = pinata.upload_to_pinata('temp.json')
        except:
            print('errore')
        print(hash)
        contratto.setTerapia(accounts[i],hash,{'from':accounts[0]})


    return contratto