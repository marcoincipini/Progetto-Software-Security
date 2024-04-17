from brownie import accounts, GestioneADI
import scripts.setup as set
import json

def main():
    contratto = GestioneADI.deploy(accounts[0],{'from':accounts[0]})
    set.utenti(contratto)
    set.conferme(contratto)
    with open('scripts/conferme.json','r') as file:
        conferme = json.load(file)
    
    operatore = int(input("Inserisci ID dell'operatore (8 - 9): "))
    while not (operatore == 8 or operatore == 9 or operatore == 0):
        operatore = int(input("Inserisci ID dell'operatore (8 - 9): "))
    while operatore!=0:
        lat = int(input("Inserisci latitudine della posizione (42): "))
        while not isinstance(lat, int):
            lat = int(input("Il valore deve essere un numero: "))
        lon = int(input("Inserisci longitudine della posizione (13): "))
        while not isinstance(lon, int):
            lon = int(input("Il valore deve essere un numero: "))
        confermeGanache = contratto.getConferme({'from':accounts[operatore]})
        for item in confermeGanache:
            for i in conferme:
                if i['ID']==item[3]:
                    print(i)
        _id = input("Inserire ID della prestazione da confermare: ")
        try:
            contratto.confermaOperatore(lat,lon,_id,{'from':accounts[8]})
        except Exception as ex:
            print("Errore rilevato nella conferma: ", ex)
        operatore = int(input("Inserisci ID dell'operatore (8 - 9): "))
        while not (operatore==8 or operatore==9 or operatore == 0):
            operatore = int(input("Inserisci ID dell'operatore (8 - 9): "))

    try:
        paziente = int(input("Inserisci ID del paziente (1-5): "))
        while paziente>5 or paziente<0:
            paziente = int(input("Inserisci ID del paziente (1-5): "))
        while paziente!=0:
            validazione = contratto.getValidazione({'from':accounts[paziente]})
            print(validazione)
            _id = input("Inserire ID della prestazione da confermare: ")
            try:
                contratto.confermaPaziente(_id,{'from':accounts[paziente]})
            except Exception as ex:
                print("Errore rilevato nella conferma: ", ex)
            paziente = int(input("Inserisci ID del paziente (1-5): "))
            while paziente>5 or paziente<0:
                paziente = int(input("Inserisci ID del paziente (1-5): "))
    except ValueError:
        print("Selezione non valida...")

    print(contratto.getConferme({'from':accounts[8]}))
    print(contratto.getConferme({'from':accounts[9]}))
    print(contratto.getValidazione({'from':accounts[1]}))
    print(contratto.getValidazione({'from':accounts[2]}))
    print(contratto.getValidazione({'from':accounts[3]}))
    print(contratto.getValidazione({'from':accounts[4]}))
    print(contratto.getValidazione({'from':accounts[5]}))