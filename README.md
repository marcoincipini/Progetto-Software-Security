# Progetto Corso Software Security and Blockchain

## Indice
- [Introduzione](#Introduzione)
- [Tecnologie utilizzate](#tecnologie-utilizzate)
- [Installazione](#installazione)
- [Funzionamento] (#funzionamento)
- [Test](#test)
- [Autori](#autori)

## Introduzione
L'applicazione è stata progettata per gestire e validare i dati medici dei pazienti che usufruiscono del servizio di Assistenza Domiciliare Integrata (ADI).
Per fare ciò è stato sviluppato uno smart contract su blockchain Ethereum per garantire privacy, correttezza e trasparenza.

## Tecnologie utilizzate
* **Python** per lo sviluppo delle demo interattive
* **Solidity** per lo sviluppo dello smart contract
* **Brownie** framework per lo sviluppo, debug e test dello smart contract
* **Ganache** per eseguire localmente una Blockchain Ethereum di test
* **Pinata** piattaforma di storage basata su IPFS
* **Docker** per la distribuzione dell'applicazione

## Installazione
Per installare ed utilizzare l'applicazione è necessario installare Brownie e Ganache. Il modo più semplice consiste nel seguire i seguenti passaggi:
### Windows
nella Powershell di Windows
'''
python3 -m pip install --user pipx 
python3 -m pipx ensurepath 
'''
oppure
'''
py -m pip install --user pipx 
py -m pipx ensurepath 
'''

chiudere e riaprire la Powershell

'''
pipx install eth-brownie
'''

Ora è necessario creare una cartella vuota dove fare il pull della repository.
Al suo interno aprire la Powershell ed eseguire
'''
brownie init 
git init 
git remote add origin https://github.com/marcoincipini/Progetto-Software-Security 
git pull origin main
brownie compile
'''
(se viene visualizzato un errore, eliminare i file che vengono riportati).

Installare Ganache dalla Powershell
'''
npm install ganache -global
'''
### Ubuntu
Installare Brownie (Richiede python3)
'''
pip install eth-brownie 
'''

Installare Ganache (Richiede NODE.js)
'''
npm install ganache --global 
'''
[Connettere Brownie a Ganache](https://eth-brownie.readthedocs.io/en/stable/network-management.html)

Configurazione di brownie e pull della repository all'interno di una nuova cartella
'''
brownie init 
git init 
git remote add origin https://github.com/marcoincipini/Progetto-Software-Security 
git pull origin main
brownie compile 
'''
### Docker
Nel caso in cui si abbia a disposizione il Dockerfile per l'installazione ed una versione funzionante di Docker e Docker Compose, l'applicazione può essere installata eseguendo
'''
docker-compose build
docker build -t gestione_adi .
'''
Può essere poi avviata con
'''
docker run -it --rm --env-file pinata.env --name adi gestione_adi
'''

## Funzionamento
Ad ogni utente è associato un account nella blockchain Ethereum che, in base al ruolo assegnato in fase di creazione (paziente, medico, operatore sanitario, ASUR) può effettuare determinate azioni.
* **Paziente non inserito nel programma ADI**: può richiedere di far parte del programma ADI, inviando una richiesta.
* **ASUR**: può visualizzare ed accettare le richieste ADI ricevute.
* **Pazienti inseriti nel programma ADI**: possono visualizzare il loro piano terapeutico. Inoltre possono accettare la conferma di effettuazione prestazione avviata dal medico o dall'operatore che ha eseguito la visita.
* **Medici**: possono visualizzare i piani terapeutici dei loro pazienti ed, al bisogno, modificarli. Possono inoltre eseguire visite presso i pazienti ed avviare il processo di conferma di effettuazione prestazione.
* **Operatori sanitari**: possono eseguire visite presso i pazienti ed avviare il processo di conferma di effettuazione prestazione.

I file relativi ai pazienti, alle attrezzature, alle conferme e ai relativi piani terapeutici sono salvati su Pinata che fornisce per ognuno un hash. Questi hash sono utilizzati per la validazione nello smart contract. 

Nella repository, oltre allo smart contract sviluppato, sono presenti demo interattive che configurano e consentono di eseguire azioni su una blockchain Ethereum di test.
Le demo possono essere eseguite con il comando
'''
brownie run scripts/NOMEDEMO.py
'''

### Demo
* *demoConferme.py* riguarda il processo di conferma di una prestazione presso il paziente. 
Il medico/operatore sanitario avvia il processo ed il paziente lo conferma.

* *demoRichiestaPaziente.py* riguarda la fase di richiesta inserimento al programma ADI. 
Il paziente manda una richiesta all'ASUR per essere aggiunto al programma ADI; L'ASUR può accettare la richiesta.

* *demoPianoTerapeutico.py* riguarda la visualizzazione e/o modifica del piano terapeutico di un paziente.
L'utente medico può visualizzare il piano terapeutico di uno dei suoi pazienti, modificarlo o aggiungere una voce. Il paziente può visualizzare il suo piano terapeutico.

* *demoValidazioneStream.py* riguarda la validazione dei dati stream ricevuti dalle attrezzature.
Le attrezzature degli utenti inviano dati relativi alla salute di questi ultimi; i dati vengono validati dal contratto.

## Test

## Autori
Il progetto è stato sviluppato dai seguenti studenti dell'Università Politecnica delle Marche:
* Marco Incipini
* Federico Paolucci
* Simone Giano