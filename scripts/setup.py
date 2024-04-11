from brownie import accounts, network, Contract, GestioneADI
import json
import scripts.pinata as pinata

def main():
    contratto=GestioneADI.deploy(accounts[0],{'from':accounts[0]})
    utenti(contratto)
    attrezzature(contratto)
    terapie(contratto)
    print(contratto.validaRilevazione(accounts[1],7043,"Monitor del ritmo cardiaco",{'from':accounts[2]}),)


def utenti(contratto):
    # Associazione degli account ai vari ruoli
    # Apertura del file contenente le informazioni sui pazienti
    with open('scripts/pazienti.json','r') as file:
        pazienti = json.load(file)
    
    # Assegnazione account 1-5 ai pazienti
    for item in pazienti:
        contratto.setPaziente(accounts[item['ID']],item['Latitudine'],item['Longitudine'],{'from':accounts[0]})
    # Assegnazione account 6-7 ai medici
    for item in range(6,8):
        contratto.setMedico(accounts[item],{'from':accounts[0]})
    # Assegnazione account 8-9 agli operatori
    for item in range(8,10):
        contratto.setOperatore(accounts[item],{'from':accounts[0]})
    # Associazione dei pazienti al relativo medico curante
    for item in range(1,6):
        i= 6 if (item%2) else 7
        contratto.setmedicoCurante(accounts[item],accounts[i])

def terapie(contratto):
    # Apertura del file contenente le terapie
    with open('scripts/terapie.json','r') as file:
        terapie = json.load(file)
    # Carico i dati delle terapie di ogni paziente
    for item in range(1,6):
        dati= list(filter(lambda x:x["IDPaziente"]==item,terapie))
        with open('temp.json','w') as file:
            json.dump(dati,file)
        hash=pinata.upload_to_pinata('temp.json')
        medicoC= 6 if (item%2) else 7
        contratto.setTerapia(accounts[item],bytes(hash,'utf-8'),{'from':accounts[medicoC]})

def conferme(contratto):
    # Apertura del file contenente le prestazioni da confermare
    with open('scripts/conferme.json','r') as file:
        conferme = json.load(file)
    # Carico i dati relativi alle conferme
    for item in conferme:
        contratto.setConferma(accounts[item['IDPaziente']],accounts[item['Operatore']],item['Procedura'],item['ID'],{'from':accounts[0]})

def attrezzature(contratto):
    # Apertura del file contenente le attrezzature
    with open('scripts/attrezzature.json','r') as file:
        attrezzature=json.load(file)
    # Carico il file attrezzature su pinata e sulla blockchain
    for item in attrezzature:
        contratto.setAttrezzatura(accounts[item['IDPaziente']],item['IDDispositivo'],item['Tipologia dispositivo'],{'from':accounts[0]})
