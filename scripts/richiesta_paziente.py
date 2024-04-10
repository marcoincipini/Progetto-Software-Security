from brownie import accounts, network, Contract, GestioneADI
import scripts.setup as set

#demo: Aggiunge un paziente e lo stesso manda una richiesta all'ASUR per essere aggiunto al programma ADI
def main():
    contratto=GestioneADI.deploy(accounts[0],{'from':accounts[0]})
    set.utenti(contratto)
    
    nuovo_ID = len(accounts)
    i = True
    while(i):
        #sono impostati i dati manualmente del nuovo paziente:
        try:
            nuovo_paziente = {
                "ID": nuovo_ID,
                "Latitudine": float(input("Inserisci la latitudine del nuovo paziente (tra 42 e 43): ")),
                "Longitudine": float(input("Inserisci la longitudine del nuovo paziente (tra 13 e 13,8): "))
            }
            if (nuovo_paziente["Latitudine"]<42 or nuovo_paziente["Latitudine"]>43 or nuovo_paziente["Longitudine"]<13 or nuovo_paziente["Longitudine"]>13.8):
                print("I dati geografici inseriti sono fuori dall'area di influenza del servizio.")
                print("Riprovare...")
            else:
                i = False
        except ValueError:
            print("Input non valido. Si prega di inserire un numero.")
        except Exception as e:
            print("Si è verificato un errore:", e)

    #viene aggiunto un accounts
    new_account = accounts.add()
    print("E' stato creato un nuovo paziente: ", accounts[nuovo_paziente['ID']])

    #viene inviata una richiesta dal paziente
    contratto.SetRichieste(accounts[nuovo_paziente['ID']], nuovo_paziente['Latitudine'], nuovo_paziente['Longitudine'], {'from': accounts[nuovo_paziente['ID']]})
    print("Il paziente ", accounts[nuovo_paziente['ID']], " ha inviato una richiesta ADI.")

    print("La lista delle richieste è:")
    print(contratto.getRichieste())

