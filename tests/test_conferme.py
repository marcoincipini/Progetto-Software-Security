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
    set.conferme(contratto)
    yield contratto

def test_conferma_operatore(setup):
    # togliere il commento alla tipologia di test che si desidera eseguire

    # setup degli elementi necessari a far funzionare la funzione di conferma dell'operatore
    with open('scripts/conferme.json','r') as file_conferme, open('scripts/pazienti.json','r') as file_pazienti:
        conferme = json.load(file_conferme)
        paziente = json.load(file_pazienti)

    setup.setTerapia(accounts[1],"Terapia X", {'from': accounts[6]})
    setup.setConferma(accounts[1], accounts[8], conferme[0]['Procedura'], conferme[0]['ID'], {'from':accounts[0]})

    """Questa riga di codice contiene un test che dovrebbe andare a buon fine, in quanto la richiesta di conferma dell'operatore
    viene fatta correttamente da un account che è operatore, con gli elementi della prestazione che sono corretti"""
    assert setup.confermaOperatore(paziente[0]['Latitudine'],paziente[0]['Longitudine'],conferme[0]['ID'],{'from':accounts[8]})    
    """Questa riga di codice contiene un test che non dovrebbe andare a buon fine, in quanto la richiesta di conferma dell'operatore
    non viene fatta correttamente da un account che è operatore (paziente in questo caso), nonostante gli elementi della prestazione 
    siano corretti"""
    # assert setup.confermaOperatore(paziente[0]['Latitudine'],paziente[0]['Longitudine'],conferme[0]['ID'],{'from':accounts[5]})
    """Questa riga di codice contiene un test che non dovrebbe andare a buon fine, in quanto la richiesta di conferma dell'operatore
    viene fatta correttamente da un account che è operatore, ma su un ID della prestazione che è inesistente. L'output aspettato dovrebbe essere
    'ID inesistente!' """
    # assert setup.confermaOperatore(paziente[0]['Latitudine'],paziente[0]['Longitudine'],2070,{'from':accounts[8]})
    """Questa riga di codice contiene un test che non dovrebbe andare a buon fine, in quanto la richiesta di conferma dell'operatore
    viene fatta da un account operatore, ma non quello associato correttamente al paziente. L'output aspettato dovrebbe essere
    'Operatore non autorizzato!' """
    #assert setup.confermaOperatore(paziente[0]['Latitudine'],paziente[0]['Longitudine'],conferme[0]['ID'],{'from':accounts[9]})
    """Questa riga di codice contiene un test che non dovrebbe andare a buon fine, in quanto la richiesta di conferma dell'operatore
    viene fatta da un account operatore corretto, ma che non è localizzato correttamente geograficamente. L'output aspettato dovrebbe essere
    'Operatore non localizzato!'"""
    #assert setup.confermaOperatore(42,1,conferme[0]['ID'],{'from':accounts[8]})

def test_conferma_paziente(setup):  
    # setup degli elementi necessari a far funzionare la funzione di conferma dell'operatore
    with open('scripts/conferme.json','r') as file_conferme, open('scripts/pazienti.json','r') as file_pazienti:
        conferme = json.load(file_conferme)
        paziente = json.load(file_pazienti)

    setup.setTerapia(accounts[1],"Terapia X", {'from': accounts[6]})

    """Questa riga di codice contiene un test che dovrebbe andare a buon fine, in quanto la richiesta di conferma del paziente
    viene fatta correttamente da un account che è paziente, con gli elementi della prestazione che sono corretti"""
    #assert setup.confermaPaziente(conferme[0]['ID'],{'from':accounts[1]})
    """Questa riga di codice contiene un test che non dovrebbe andare a buon fine, in quanto la richiesta di conferma del paziente
    viene fatta da un account che non è paziente (ASUR in questo caso), con gli elementi della prestazione che sono corretti"""
    #assert setup.confermaPaziente(conferme[0]['ID'],{'from':accounts[0]})
    """Questa riga di codice contiene un test che non dovrebbe andare a buon fine, in quanto la richiesta di conferma del paziente
    viene fatta correttamente da un account che è paziente, ma su un ID della prestazione che è inesistente. L'output aspettato dovrebbe essere
    'ID inesistente!' """
    assert setup.confermaPaziente(2070,{'from':accounts[1]})



