"""
demo: l'operatore indica l'esecuzione di una prestazione presso un paziente
il paziente conferma la prestazione selezionata dall'operatore
"""
import json
from brownie import accounts, GestioneADI
import scripts.setup as set


def main():
    """
    Demo: parte principale
    """
    contratto = GestioneADI.deploy(accounts[0], {"from": accounts[0]})
    set.utenti(contratto)
    set.conferme(contratto)
    with open("scripts/conferme.json", "r") as file:
        conferme = json.load(file)

    print(
        "inserire ID operatore per confermare le prestazioni, 0 per passare a conferma paziente.\n"
    )
    # selezione di un operatore che deve indicare
    # quale tra le prestazioni da eseguire vuole confermare
    operatore = int(input("Inserisci ID dell'operatore (8 - 9): \n"))
    while not (operatore == 8 or operatore == 9 or operatore == 0):
        print(
            "inserire ID operatore per confermare le prestazioni, 0 per conferma paziente.\n"
        )
        operatore = int(input("Inserisci ID dell'operatore (8 - 9):\n"))
    while operatore != 0:
        lat = int(
            input("Inserisci latitudine della posizione (42):\n")
        )  # non c'è un controllo se il valore è 42 o meno
        while not isinstance(lat, int):
            lat = int(input("Il valore deve essere un numero:\n"))
        lon = int(
            input("Inserisci longitudine della posizione (13):\n")
        )  # non c'è un controllo se il valore è 13 o meno
        while not isinstance(lon, int):
            lon = int(input("Il valore deve essere un numero:\n"))
        confermeGanache = contratto.getConferme({"from": accounts[operatore]})
        for item in confermeGanache:
            for i in conferme:
                if i["ID"] == item[3]:
                    print(i)
        _id = input(
            "Inserire ID della prestazione da confermare:\n"
        )  # l'ID della prestazione è quella indicata nel JSON
        try:
            contratto.confermaOperatore(lat, lon, _id, {"from": accounts[operatore]})
        except Exception as ex:
            print("Errore rilevato nella conferma: ", ex)
        print(
            "inserire ID operatore per confermare le prestazioni, 0 per conferma paziente.\n"
        )
        operatore = int(input("Inserisci ID dell'operatore (8 - 9):\n"))
        while not (operatore == 8 or operatore == 9 or operatore == 0):
            print(
                "inserire ID operatore per confermare le prestazioni, 0 per conferma paziente.\n"
            )
            operatore = int(input("Inserisci ID dell'operatore (8 - 9):\n"))

    # selezione di un paziente che deve confermare
    # l'esecuzione della prestazione indicata dall'operatore
    try:
        print(
            "inserire ID paziente per confermare le prestazioni, 0 per terminare\n"
        )
        paziente = int(input("Inserisci ID del paziente (1-5)\n"))
        while paziente > 5 or paziente < 0:
            print(
                "inserire ID paziente per confermare le prestazioni, 0 per terminare\n"
            )
            paziente = int(input("Inserisci ID del paziente (1-5)\n"))
        while paziente != 0:
            validazione = contratto.getValidazione({"from": accounts[paziente]})
            print(validazione)
            _id = input(
                "Inserire ID della prestazione da confermare, 0 se non sono presenti prestazioni:\n"
            )
            try:
                contratto.confermaPaziente(_id, {"from": accounts[paziente]})
            except Exception as ex:
                print("Errore rilevato nella conferma: ", ex)
            print(
                "inserire ID paziente per confermare le prestazioni, 0 per terminare\n"
            )
            paziente = int(input("Inserisci ID del paziente (1-5):\n"))
            while paziente > 5 or paziente < 0:
                print(
                    "inserire ID paziente per confermare le prestazioni, 0 per terminare\n"
                )
                paziente = int(input("Inserisci ID del paziente (1-5):\n"))
    except ValueError:
        print("Selezione non valida...")

    # stampa l'attuale situazione della blockchain
    # conferme:
    print(contratto.getConferme({"from": accounts[8]}))
    print(contratto.getConferme({"from": accounts[9]}))
    # transazioni in sospeso per ogni utente:
    print(contratto.getValidazione({"from": accounts[1]}))
    print(contratto.getValidazione({"from": accounts[2]}))
    print(contratto.getValidazione({"from": accounts[3]}))
    print(contratto.getValidazione({"from": accounts[4]}))
    print(contratto.getValidazione({"from": accounts[5]}))
