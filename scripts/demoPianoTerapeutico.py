from brownie import accounts, network, Contract, GestioneADI
import scripts.setup as set
import scripts.pinata as pinata
import json

def main():
    contratto=GestioneADI.deploy(accounts[0],{'from':accounts[0]})
    set.utenti(contratto)
    set.terapie(contratto)
    menu1 = True
    while(menu1):
        try:
            scelta = int(input("Seleziona azione (0: Utente medico - Visualizza/Aggiungi terapia; 1: Utente Paziente - Visualizza piano terapeutico; altro intero: esci): "))
            #Utente medico
            if(scelta==0):
                medici = contratto.getMedici({'from': accounts[0]})
                for i, medico in enumerate(medici):
                        print(f"{i + 1}: {medico}")
                try:
                    selezione = int(input("Seleziona ID dell'utente medico: "))
                    if 1 <= selezione <= len(medici):
                        indirizzo_med = medici[selezione-1]
                        pazienti_med = contratto.getPazientiDelMedico(indirizzo_med, {'from': accounts[0]})
                    else:
                        print("Selezione non valida.")                    
                except ValueError:
                    print("Input non valido. Inserisci un numero intero.")
                
                for i, paziente_med in enumerate(pazienti_med):
                        print(f"{i + 1}: {paziente_med}")
                try:
                    selezione = int(input("Seleziona ID del paziente: "))
                    if 1 <= selezione <= len(pazienti_med):
                        indirizzo_paz = pazienti_med[selezione-1]
                        print(indirizzo_paz)
                    else:
                        print("Selezione non valida.")                    
                except ValueError:
                    print("Input non valido. Inserisci un numero intero.")

                hash_terapia = contratto.getTerapia(indirizzo_paz, {'from': indirizzo_med})
                
                #visualizzazione e modifica json:
                json_terapia = pinata.get_file_from_pinata(hash_terapia) #json scaricato
                for i,elemento in enumerate(json_terapia):
                    print(f"{i+1}: {elemento}")

                try:
                    selezione = int(input("Seleziona azione (0: Modifica piano terapeutico; 1: Aggiungi nuova terapia; altro intero: esci): "))
                    if (selezione == 0):
                        try:
                            id_terapia = int(input("Seleziona ID della terapia: "))
                            if id_terapia >= 1 and id_terapia <= len(json_terapia):
                                terapia_selezionata = json_terapia[id_terapia - 1]
                                print("Terapia selezionata:", terapia_selezionata)
                                
                                #modifica terapia
                                for chiave, valore in terapia_selezionata.items():
                                    if chiave in ["IDPaziente", "Nome", "Cognome"]: #salto chiavi da non modificare
                                        pass
                                    else:
                                        nuovo_valore = input(f"Modifica elemento {chiave} (default: {valore}): ")
                                        if nuovo_valore:
                                            terapia_selezionata[chiave] = nuovo_valore
                                print("Terapia modificata:", terapia_selezionata)

                                #upload su pinata e su blockchain
                                with open("temp.json", "w") as file:
                                    json.dump(json_terapia, file)
                                hash = pinata.upload_to_pinata("temp.json")
                                contratto.setTerapia(indirizzo_paz,bytes(hash,'utf-8'),{'from':indirizzo_med})
                                hash_terapia = contratto.getTerapia(indirizzo_paz, {'from': indirizzo_med})
                            else:
                                print("ID terapia non valido.")
                        except ValueError:
                            print("Input non valido. Inserisci un numero intero")
                    
                    elif (selezione == 1):
                        temp = json_terapia[0]
                        nuova_terapia = {}
                        nuova_terapia["IDPaziente"] = temp["IDPaziente"]
                        nuova_terapia["Nome"] = temp["Nome"]
                        nuova_terapia["Cognome"] = temp["Cognome"]
                        for chiave in ["Operatore", "Data inizio", "Data fine", "Medicina", "Dosaggio", "Procedura"]:
                            flag = True
                            while flag:
                                nuovo_valore = input(f"Inserisci {chiave}: ")
                                if nuovo_valore:
                                    nuova_terapia[chiave] = nuovo_valore
                                    flag = False
                                else:
                                    print("Devi inserire un valore!")
                        json_terapia.append(nuova_terapia)
                        #upload su pinata e su blockchain
                        with open("temp.json", "w") as file:
                            json.dump(json_terapia, file)
                        hash = pinata.upload_to_pinata("temp.json")
                        contratto.setTerapia(indirizzo_paz,bytes(hash,'utf-8'),{'from':indirizzo_med})
                        hash_terapia = contratto.getTerapia(indirizzo_paz, {'from': indirizzo_med})
                except ValueError:
                    print("Scelta non valida... inserisci un numero intero.")

            #Utente paziente 
            elif(scelta==1):
                pazienti = contratto.getPazienti({'from': accounts[0]})
                for i, paziente in enumerate(pazienti):
                    print(f"{i + 1}: {paziente}")
                try:
                    selezione = int(input("Seleziona ID del paziente: "))
                    if 1 <= selezione <= len(pazienti):
                        paz = pazienti[selezione-1]
                        indirizzo_paz = paz[0]
                        hash_terapia = contratto.getTerapia(indirizzo_paz, {'from': indirizzo_paz})
                
                        #visualizzazione json
                        json_terapia = pinata.get_file_from_pinata(hash_terapia)
                        for i,elemento in enumerate(json_terapia):
                            print(f"{i+1}: {elemento}")
                    else:
                        print("Selezione non valida.")                    
                except ValueError:
                    print("Input non valido. Inserisci un numero intero.")

            #Uscita
            else:
                print("Uscita...")
                menu1=False
        except ValueError:
            print("Scelta non valida... inserisci un numero intero.")