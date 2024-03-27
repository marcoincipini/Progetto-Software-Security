from brownie import accounts, network, Contract, GestioneADI
import json
import pinata

# Devo sempre definire un metodo main
# Il setup serve a sviluppare il contratto da utilizzare ed inserire i dati iniziali.
def main():
    # Deploy del contratto GestioneADI con l'account principale
    contratto=GestioneADI.deploy(accounts[0],{'from':accounts[0]})
    #contratto.setPaziente(accounts[1],10,10)
    
    # Associazione degli account ai vari ruoli
    with open('scripts/pazienti.json','r') as file:
        pazienti = json.load(file)
    
    for item in pazienti:
        contratto.setPaziente(accounts[item['ID']],item['Latitudine'],item['Longitudine'],{'from':accounts[0]})
    for item in range(6,8):
        contratto.setMedico(accounts[item],{'from':accounts[0]})
    for item in range(8,10):
        contratto.setOperatore(accounts[item],{'from':accounts[0]})
    
    for item in range(1,6):
        i= 6 if (item%2) else 7
        print(i)
        contratto.setmedicoCurante(accounts[item],accounts[i])
        print(item)

    # Creazione di un set di dati di prova per ogni struttura
    with open('scripts/terapie.json','r') as file:
        terapie = json.load(file)
    for item in range(1,6):
        dati= list(filter(lambda x:x["IDPaziente"]==item,terapie))
        with open('temp.json','w') as file:
            json.dump(dati,file)
        hash=pinata.upload_to_pinata('temp.json')
        medicoC= 6 if (item%2) else 7
        contratto.setTerapia(accounts[item],bytes(hash,'utf-8'),{'from':accounts[medicoC]})
        #print(pinata.get_file_from_pinata(hash))
        # contratto.setTerapia(accounts[i],hash,{'from':accounts[0]})
    res= contratto.getTerapia(accounts[1],{'from':accounts[1]})
    print(type(res))
    print(res)

    with open('scripts/conferme.json','r') as file:
        conferme = json.load(file)
    for item in conferme:
        contratto.setConferma(accounts[item['IDPaziente']],accounts[item['Operatore']],item['Procedura'])


    return contratto
