from brownie import accounts, GestioneADI
import scripts.setup as set
import time
import random
import json

INTERVALLO=5

def main():
    contratto=GestioneADI.deploy(accounts[0],{'from':accounts[0]})
    set.utenti(contratto)
    set.attrezzature(contratto)
    with open('scripts/attrezzature.json','r') as file:
        attrezzature=json.load(file)
    while True:
        i=random.randint(1,5)-1
        print("L'utente ", accounts[i+1], "sta inserendo un dato relativo al dispositivo:")
        print(attrezzature[i])
        a=attrezzature[i]
        if i==4:
            try:
                v=contratto.validaRilevazione(accounts[a['IDPaziente']],a['IDDispositivo'],a['Tipologia dispositivo'],{'from':accounts[i]})
            except Exception as ex:
                v=ex
        else:
            v=contratto.validaRilevazione(accounts[a['IDPaziente']],a['IDDispositivo'],a['Tipologia dispositivo'],{'from':accounts[i+1]})
        print("Il processo di validazione ha dato esito", v)
        time.sleep(INTERVALLO)