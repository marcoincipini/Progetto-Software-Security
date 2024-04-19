from brownie import accounts, network, Contract, GestioneADI
import scripts.setup as set

#demo: Il paziente manda una richiesta all'ASUR per essere aggiunto al programma ADI
#      L'ASUR può accettare il paziente che ha inviato la richiesta.

def main():
    contratto=GestioneADI.deploy(accounts[0],{'from':accounts[0]})
    set.utenti(contratto)
    menu = True
    while(menu):
        try:
            scelta = int(input("Seleziona azione (0: Invia una richiesta come nuovo paziente; 1: Visualizza/accetta richieste con l'utente ASUR; altro intero: esci): "))
            # Selezione di invio richiesta come nuovo paziente
            if(scelta==0):
                nuovo_ID = len(accounts) #l'ID dell'account è impostato in modo che sia la posizione successiva all'ultima
                i = True # flag per mantenere attivo il loop di input in caso di errori
                while(i):
                    # sono impostati manualmente i dati del nuovo paziente:
                    try:
                        nuovo_paziente = {
                            "ID": nuovo_ID,
                            "Latitudine": int(input("Inserisci la latitudine del nuovo paziente (42 - 43): ")),
                            "Longitudine": int(input("Inserisci la longitudine del nuovo paziente (13): "))
                        }
                        # controllo che il paziente inserito sia localizzato nelle Marche (lat 42-43 lon 13)
                        if (nuovo_paziente["Latitudine"]<42 or nuovo_paziente["Latitudine"]>43 or nuovo_paziente["Longitudine"]<13 or nuovo_paziente["Longitudine"]>13.8):
                            print("I dati geografici inseriti sono fuori dall'area di influenza del servizio.")
                            print("Riprovare...")
                        else:
                            i = False
                    except ValueError:
                        print("Input non valido. Si prega di inserire un numero intero.")
                    except Exception as e:
                        print("Si è verificato un errore:", e)

                # viene aggiunto un account
                accounts.add()
                print("E' stato creato un nuovo paziente: ", accounts[nuovo_paziente['ID']])

                # viene inviata una richiesta dal paziente
                contratto.SetRichieste(accounts[nuovo_paziente['ID']], nuovo_paziente['Latitudine'], nuovo_paziente['Longitudine'], {'from': accounts[nuovo_paziente['ID']]})
                print("Il paziente ", accounts[nuovo_paziente['ID']], " ha inviato una richiesta ADI.")

            # Selezione per accettare le richieste ADI di nuovi utenti da parte dell'ASUR
            elif scelta == 1:
                richieste = contratto.getRichieste() # ottiene tutte le richieste ancora non accettate
                if not richieste:
                    print("Non ci sono richieste da visualizzare.")
                else:
                    print("La lista delle richieste è:")
                    for i, richiesta in enumerate(richieste):
                        print(f"{i + 1}: {richiesta}")

                    try:
                        selezione = int(input("Inserisci il numero corrispondente alla richiesta che desideri accettare: "))
                        if 1 <= selezione <= len(richieste):
                            indice = selezione - 1
                            indirizzo_pz, lat_pz, lon_pz = richieste[indice]
                            contratto.setPazienteASUR(indirizzo_pz,lat_pz,lon_pz,indice, {'from': accounts[0]}) # viene accettata la richiesta
                            print(f"Hai inserito il paziente {indirizzo_pz} al programma ADI")
                        else:
                            print("Selezione non valida.")
                    except ValueError:
                        print("Input non valido. Inserisci un numero intero.")
            else:
                print("Uscita...")
                menu=False
        except ValueError:
            print("Scelta non valida... inserisci un numero intero.")
