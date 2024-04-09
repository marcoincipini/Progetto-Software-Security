from brownie import accounts, network, Contract, GestioneADI
import scripts.setup as set

#demo: Aggiunge un paziente e lo stesso manda una richiesta all'ASUR per essere aggiunto al programma ADI
def main():
    contratto=GestioneADI.deploy(accounts[0],{'from':accounts[0]})
    set.utenti(contratto)
    
    #sono impostati i dati del nuovo paziente:
    nuovo_paziente = {
        "ID": 10,
        "Latitudine": 42.86,
        "Longitudine": 13.05
    }
    #viene aggiunto un accounts
    new_account = accounts.add()
    print("E' stato creato un nuovo paziente: ", accounts[nuovo_paziente['ID']])

    #viene inviata una richiesta dal paziente
    contratto.SetRichieste(accounts[nuovo_paziente['ID']], nuovo_paziente['Latitudine'], nuovo_paziente['Longitudine'], {'from': accounts[nuovo_paziente['ID']]})
    print("Il paziente ", accounts[nuovo_paziente['ID']], " ha inviato una richiesta ADI.")

    print("La lista delle richieste è:")
    print(contratto.getRichieste())

