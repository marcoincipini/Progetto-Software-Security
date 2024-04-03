from brownie import accounts, network, Contract, GestioneADI
import json
import pinata
import setup

#demo: Aggiunge un paziente e lo stesso manda una richiesta all'ASUR per essere aggiunto al programma ADI
def main():
    contratto=GestioneADI.deploy(accounts[0],{'from':accounts[0]})
    setup.utenti(contratto)
    #sono impostati i dati del nuovo paziente:
    nuovo_paziente = {
        "ID": 10,
        "Latitudine": 42.86,
        "Longitudine": 13.05
    }
    #viene aggiunto un accounts
    new_account = accounts.add()

    #viene inviata una richiesta dal paziente
    contratto.setRichieste(accounts[nuovo_paziente['ID']], nuovo_paziente['Latitudine'], nuovo_paziente['Longitudine'], {'from': accounts[nuovo_paziente['ID']]})