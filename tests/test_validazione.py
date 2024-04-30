import pytest
import scripts.setup as set
import json
from brownie import GestioneADI, accounts

# Funzione di setup che viene eseguita prima di ogni test
@pytest.fixture(scope="module", autouse=True)
def setup():
    # Deploy del contratto GestioneADI prima di ogni test
    contratto =  GestioneADI.deploy(accounts[0],{'from':accounts[0]})
    # setup degli utenti che servono per gestire gli account delle funzioni usate da questi test
    set.utenti(contratto)
    set.attrezzature(contratto)
    yield contratto

def test_valida_rilevazione(setup):
    # togliere il commento alla tipologia di test che si desidera eseguire
    
    with open('scripts/attrezzature.json','r') as file_attrezzature:
        attrezzature = json.load(file_attrezzature)

    """Questa riga di codice contiene un test che dovrebbe andare a buon fine, in quanto la richiesta di validazione della rilevazione da parte
    dell'attrezzature viene fatta da un account paziente sull'account per il quale è autorizzato"""
    assert setup.validaRilevazione(accounts[1], attrezzature[0]['IDDispositivo'],attrezzature[0]['Tipologia dispositivo'], {'from':accounts[1]})
    """Questa riga di codice contiene un test che non dovrebbe andare a buon fine, in quanto la richiesta di validazione della rilevazione da parte
    dell'attrezzature viene fatta da un account paziente su un account paziente per il quale non dispone dell'autorizzazione. L'output
    aspettato dovrebbe essere 'Paziente non autorizzato' """
    #assert setup.validaRilevazione(accounts[1], attrezzature[0]['IDDispositivo'],attrezzature[0]['Tipologia dispositivo'], {'from':accounts[2]})
    """Questa riga di codice contiene un test che non dovrebbe andare a buon fine, in quanto la richiesta di validazione della rilevazione da parte
    dell'attrezzature viene fatta da un account paziente su un account che non è paziente, quindi viene visto come inesistente. L'output
    aspettato dovrebbe essere 'Paziente inesistente' """
    #assert setup.validaRilevazione(accounts[7], attrezzature[0]['IDDispositivo'],attrezzature[0]['Tipologia dispositivo'], {'from':accounts[1]})