# Progetto Corso Software Security and Blockchain

## Indice
- [Introduzione](#intro)
- [Tecnologie utilizzate](#tech)
- [Installazione](#install)
- [Funzionamento](#usage)
- [Test](#test)
- [Autori](#autors)

<a name="intro"></a>
## Introduzione
L'applicazione è stata progettata per gestire e validare i dati medici dei pazienti che usufruiscono del servizio di Assistenza Domiciliare Integrata (ADI).
Per fare ciò è stato sviluppato uno smart contract su blockchain Ethereum per garantire privacy, correttezza e trasparenza.

<a name="tech"></a>
## Tecnologie utilizzate
* **Solidity** per lo sviluppo dello smart contract
* **Python** per lo sviluppo delle demo interattive
* **Brownie** framework per lo sviluppo, debug e test dello smart contract
* **Ganache** per eseguire localmente una Blockchain Ethereum di test
* **Pinata** piattaforma di storage basata su IPFS
* **Docker** per la distribuzione dell'applicazione

<a name="install"></a>
## Installazione
Per installare ed utilizzare l'applicazione è necessario installare Brownie e Ganache. Il modo più semplice consiste nel seguire i seguenti passaggi:
### Windows
nella Powershell di Windows
```
python3 -m pip install --user pipx 
python3 -m pipx ensurepath 
```
oppure
```
py -m pip install --user pipx 
py -m pipx ensurepath 
```

chiudere e riaprire la Powershell

```
pipx install eth-brownie
```

Ora è necessario creare una cartella vuota dove fare il pull della repository.
Al suo interno aprire la Powershell ed eseguire
```
git init 
git remote add origin https://github.com/marcoincipini/Progetto-Software-Security 
git pull origin main
brownie compile
```

Installare Ganache dalla Powershell
```
npm install ganache -global
```
### Ubuntu
Per installare l'applicativo è possibile scaricare il file linux_gestioneadi.sh ed eseguirlo. Per dare i privilegi di esecuzione allo script usare il comando:
```
chmod +x linux_gestioneadi.sh
```

Per eseguire lo script usare il comando:
```
./linux_gestioneadi.sh
```

Per verificare la corretta installazione eseguire il comando:
```
brownie test
```

Per eseguire le demo inserire il file .env nella cartella di progetto (rinominandolo .env)
### Docker
E possibile eseguire il progetto in un container scaricando il file docker.
Avendo a disposizione il Dockerfile per l'installazione ed una versione funzionante di Docker e Docker Compose, l'applicazione può essere installata eseguendo
```
docker-compose build
docker build -t gestione_adi .
```
Può essere poi avviata con
```
docker run -it --rm --env-file pinata.env --name adi gestione_adi
```
<a name="usage"></a>
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
```
brownie run scripts/NOMEDEMO.py
```

### Demo
* *demoConferme.py* riguarda il processo di conferma di una prestazione presso il paziente. 
Il medico/operatore sanitario avvia il processo ed il paziente lo conferma.
```
brownie run scripts/demoConferme.py
```

* *demoRichiestaPaziente.py* riguarda la fase di richiesta inserimento al programma ADI. 
Il paziente manda una richiesta all'ASUR per essere aggiunto al programma ADI; L'ASUR può accettare la richiesta.
```
brownie run scripts/demoRichiestePaziente.py
```

* *demoPianoTerapeutico.py* riguarda la visualizzazione e/o modifica del piano terapeutico di un paziente.
L'utente medico può visualizzare il piano terapeutico di uno dei suoi pazienti, modificarlo o aggiungere una voce. Il paziente può visualizzare il suo piano terapeutico.
```
brownie run scripts/demoPianoTerapeutico.py
```

* *demoValidazioneStream.py* riguarda la validazione dei dati stream ricevuti dalle attrezzature.
Le attrezzature degli utenti inviano dati relativi alla salute di questi ultimi; i dati vengono validati dal contratto.
```
brownie run scripts/demoValidazioneStream.py
```

<a name="test"></a>
## Test
Per verificare il corretto funzionamento del contratto sviluppato sono stati creati dei test specifici.
I test possono essere avviati singolarmente con
```
brownie test tests/NOMETEST.py
```
nello specifico:
```
brownie test tests/test_conferme.py
```
```
brownie test tests/test_getter.py
```
```
brownie test tests/test_setter.py
```
```
brownie test tests/test_validazione.py
```

Possono essere avviati tutti i test con
```
brownie test
```

<a name="autors"></a>
## Autori
Il progetto è stato sviluppato dai seguenti studenti dell'Università Politecnica delle Marche:
* Marco Incipini
* Federico Paolucci
* Simone Giano
