import json

filediprova='scripts/prova.json'
with open(filediprova,'r') as file:
    data = json.load(file)

for i in data:
    print(i["indirizzo"]["città"])
    for j in i["amici"]:
        print(j)
    print(i["amici"])

# Per inserire un dato devo formattarlo come un json
# Quindi mettere in una funzione questo codice
# devo usare dizionari per gli oggetti vedi lezione PA-15-03-24
dati = {
    "a": "pippo",
    "b": "pippo",
    "c": "pippo"
    }

with open('scripts/ins.json', "a") as file:
    json.dump(dati, file, indent=4)

# a - append
# w - sovrascrive