from brownie import accounts, network, Contract, GestioneADI
import scripts.setup as set
import scripts.pinata as pinata
import json
import datetime
'''
demo: L'utente medico può visualizzare il piano terapeutico di uno dei suoi pazienti, modificarlo o aggiungere una voce.
    Il paziente può visualizzare il suo piano terapeutico.
'''
def main():
    contratto=GestioneADI.deploy(accounts[0],{'from':accounts[0]})
    set.utenti(contratto)
    set.terapie(contratto)
    menu1 = True # flag per mantenere la selezione principale in loop
    menu2 = False # flag per consentire l'accesso al menu di modifica del piano terapeutico se gli ID del medico e del paziente sono validi
    while(menu1):
        try:
            scelta = int(input("Seleziona azione (0: Utente medico - Visualizza/Aggiungi terapia; 1: Utente Paziente - Visualizza piano terapeutico; altro intero: esci):\n "))
            #Utente medico
            if(scelta==0):
                medici = contratto.getMedici({'from': accounts[0]})
                for i, medico in enumerate(medici): # visualizzo tutti i medici per la selezione
                        print(f"{i + 1}: {medico}")
                try:
                    selezione = int(input("Seleziona ID dell'utente medico:\n"))
                    if 1 <= selezione <= len(medici): # se la selezione è valida consento la selezione di un paziente associato
                        print("accesso effettuato come account Medico\n")
                        indirizzo_med = medici[selezione-1]
                        pazienti_med = contratto.getPazientiDelMedico({'from': indirizzo_med}) # ottengo tutti i pazienti associati al medico
                        for i, paziente_med in enumerate(pazienti_med): # visualizzo tutti i pazienti associati al medico
                            print(f"{i + 1}: {paziente_med}")
                        try:
                            selezione = int(input("Seleziona ID del paziente: ")) # seleziono il paziente
                            if 1 <= selezione <= len(pazienti_med):
                                indirizzo_paz = pazienti_med[selezione-1]
                                print(indirizzo_paz)
                                menu2 = True # consente l'accesso al menu di modifica
                            else:
                                print("Selezione non valida.\n")                    
                        except ValueError:
                            print("Input non valido. Inserisci un numero intero.\n")
                    else:
                        print("Selezione non valida.\n")                    
                except ValueError:
                    print("Input non valido. Inserisci un numero intero.\n")
                
                # menu di modifica (posso accedere solo se gli ID del medico e del paziente sono validi)
                if(menu2):
                    # ottengo l'hash della terapia e scarico il file json associato da pinata
                    hash_terapia = contratto.getTerapia(indirizzo_paz, {'from': indirizzo_med})
                    json_terapia = visualizzaJson(hash_terapia)

                    try:
                        selezione = int(input("Seleziona azione (0: Modifica piano terapeutico; 1: Aggiungi nuova terapia; altro intero: esci):\n"))
                        # selezione modifica di una delle voci del piano terapeutico
                        if (selezione == 0):
                            try:
                                id_terapia = int(input("Seleziona ID della terapia:\n")) # seleziona id della terapia da modificare
                                if id_terapia >= 1 and id_terapia <= len(json_terapia):
                                    terapia_selezionata = json_terapia[id_terapia - 1]
                                    print("Terapia selezionata: ", terapia_selezionata)
                                    
                                    # modifica terapia
                                    for chiave, valore in terapia_selezionata.items():
                                        if chiave in ["IDPaziente", "Nome", "Cognome"]: # salto chiavi da non modificare
                                            pass
                                        else:
                                            nuovo_valore = input(f"Modifica elemento {chiave} (default: {valore}): ")
                                            if checkValore(nuovo_valore,chiave): # valida il valore inserito
                                                terapia_selezionata[chiave] = nuovo_valore
                                            else:
                                                if nuovo_valore:
                                                    print("Valore non valido! Verrà mantenuto il valore di default.\n")
                                    print("Terapia modificata: ", terapia_selezionata)
                                    # upload su pinata e su blockchain
                                    uploadTerapia(contratto,json_terapia,indirizzo_paz,indirizzo_med)
                                else:
                                    print("ID terapia non valido.\n")
                            except ValueError:
                                print("Input non valido. Inserisci un numero intero.\n")
                        # selezione di aggiunta nuova voce al piano terapeutico
                        elif (selezione == 1):
                            temp = json_terapia[0]
                            nuova_terapia = {}
                            nuova_terapia["IDPaziente"] = temp["IDPaziente"]
                            nuova_terapia["Nome"] = temp["Nome"]
                            nuova_terapia["Cognome"] = temp["Cognome"] # ID, nome, cognome sono preimpostati
                            for chiave in ["Operatore", "Data inizio", "Data fine", "Medicina", "Dosaggio", "Procedura"]:
                                flag = True # flag per mantenere il loop di inserimento attivo in caso di input errato
                                while flag:
                                    nuovo_valore = input(f"Inserisci {chiave}: ")
                                    if checkValore(nuovo_valore, chiave):
                                        nuova_terapia[chiave] = nuovo_valore
                                        flag = False
                                    else:
                                        print("Inserisci un valore valido!\n")
                            json_terapia.append(nuova_terapia) # aggiunge la voce al json del piano terapeutico
                            #upload su pinata e su blockchain
                            uploadTerapia(contratto,json_terapia,indirizzo_paz,indirizzo_med)
                    except ValueError:
                        print("Scelta non valida... inserisci un numero intero.\n")
                menu2 = False # reset della selezione

            # Scelta dell'utente paziente - visualizzazione json
            elif(scelta==1):
                pazienti = contratto.getPazienti({'from': accounts[0]}) 
                for i, paziente in enumerate(pazienti): # visualizza tutti i pazienti
                    print(f"{i + 1}: {paziente}")
                try:
                    selezione = int(input("Seleziona ID del paziente:\n "))
                    if 1 <= selezione <= len(pazienti):
                        print("accesso effettuato come account paziente\n")
                        paz = pazienti[selezione-1]
                        indirizzo_paz = paz[0]
                        hash_terapia = contratto.getTerapia(indirizzo_paz, {'from': indirizzo_paz})
                        # visualizza il json corrispondente
                        visualizzaJson(hash_terapia)
                    else:
                        print("Selezione non valida.")                    
                except ValueError:
                    print("Input non valido. Inserisci un numero intero.\n")

            #Uscita
            else:
                print("Uscita...")
                menu1=False
        except ValueError:
            print("Scelta non valida... inserisci un numero intero.\n")

# funzione per ottenere il file da pinata tramite l'hash e visualizzarlo
def visualizzaJson(hash):
    json_terapia = pinata.get_file_from_pinata(hash)
    for i,elemento in enumerate(json_terapia):
        print(f"{i+1}: {elemento}")
    return json_terapia

# funzione per upload del json modificato su pinata e upload dell'hash associato sulla blockchain
def uploadTerapia(contratto, json_terapia, indirizzo_paz, indirizzo_med):
    with open("temp.json", "w") as file:
        json.dump(json_terapia, file)
    hash = pinata.upload_to_pinata("temp.json")
    contratto.setTerapia(indirizzo_paz,bytes(hash,'utf-8'),{'from':indirizzo_med})

# funzione di controllo del valore inserito in input
def checkValore(nuovo_valore, chiave):
    if nuovo_valore:
        if chiave in ["Operatore", "Medicina"]:
            if len(nuovo_valore) <= 50:
                return True
            else:
                return False
        elif chiave in ["Data inizio", "Data fine"]:
            try:
                datetime.datetime.strptime(nuovo_valore, '%d/%m/%Y') # controllo sulla data
                return True
            except ValueError:
                return False
        elif chiave == "Dosaggio":
            if len(nuovo_valore) <= 20:
                return True
            else:
                return False
        elif chiave == "Procedura":
            if len(nuovo_valore) <= 500:
                return True
            else:
                return False
        else:
            print("Chiave non contemplata...\n")
            return False
    else:
        return False