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

def test_get_conferme(setup):
    """questa riga di codice contiene un test che dovrebbe andare a buon fine, dato che la richiesta di avere una conferma
    avviene da un account operatore, come dovrebbe essere"""
    assert setup.getConferme({'from':accounts[8]})

def test_get_conferme_ex(setup):
    """questa riga di codice contiene un test che non dovrebbe andare a buon fine, dato che la richiesta di avere una conferma
    avviene da un account non operatore (medico in questo caso). L'output aspettato sarebbe 'Utente senza privilegi necessari,
    provare con account operatore' """
    with pytest.raises(Exception):
        setup.getConferme({'from':accounts[6]})
     
def test_get_validazione(setup):
    """queste righe di codice contengono un test che dovrebbe andare a buon fine, dato che la richiesta di avere una validazione 
    avviene da un account corretto (operatore), e la prestazione da confermare ha i parametri corretti"""
    with open('scripts/conferme.json','r') as file_conferme, open('scripts/pazienti.json','r') as file_pazienti:
        conferme = json.load(file_conferme)
        paziente = json.load(file_pazienti)
        
    setup.confermaOperatore(paziente[0]['Latitudine'],paziente[0]['Longitudine'],conferme[0]['ID'],{'from':accounts[8]})
    assert setup.getValidazione({'from':accounts[1]})

def test_get_validazione_ex(setup):
    """questa riga di codice contiene un test che non dovrebbe andare a buon fine, dato che la richiesta di avere una validazione
    avviene da un account non paziente (account ASUR in questo caso). L'output aspettato dovrebbe essere 'Utente senza privilegi necessari,
    provare con account paziente'"""
    with pytest.raises(Exception):
        setup.getValidazione({'from':accounts[0]})

def test_get_medici(setup):
    """questa riga di codice contiene un test che dovrebbe andare a buon fine, dato che la richiesta per vedere i medici
    avviene da un account ASUR, come dovrebbe essere"""
    assert setup.getMedici({'from':accounts[0]})

def test_get_medici_ex(setup):
    """questa riga di codice contiene un test che non dovrebbe andare a buon fine, dato che la richiesta per vedere i medici
    avviene da un account non ASUR (operatore in questo caso). L'output aspettato sarebbe 'Utente senza privilegi necessari' """
    with pytest.raises(Exception):
        setup.getMedici({'from':accounts[8]})

def test_get_pazienti_del_medico(setup):
    """questa riga di codice contiene un test che dovrebbe andare a buon fine, dato che la richiesta per la visualizzazione dei pazienti
    di un determinato medico (in questo caso quello associato all'account 6), avviene da un account ASUR, come dovrebbe essere"""
    assert setup.getPazientiDelMedico({'from':accounts[6]})

def test_get_pazienti_del_medico_ex(setup):
    """questa riga di codice contiene un test che non dovrebbe andare a buon fine, dato che la richiesta per la visualizzazione dei pazienti
    di un determinato medico (in questo caso quello associato all'account 6),avviene da un account non ASUR (operatore in questo caso). 
    L'output aspettato sarebbe 'Utente senza privilegi necessari' """
    with pytest.raises(Exception):
        setup.getPazientiDelMedico({'from':accounts[8]})

def test_get_terapia(setup):
    """righe di codice contententi il setup della terapia, necessario per poterla visualizzare"""
    setup.setTerapia(accounts[1],"Terapia X", {'from': accounts[6]})
    
    """questa riga di codice contiene un test che dovrebbe andare a buon fine, in quanto la richiesta di vedere una terapia di un paziente
    viene fatta dall'account del suo medico curante, come dovrebbe essere"""
    assert setup.getTerapia(accounts[1], {'from':accounts[6]})

def test_get_terapia_1(setup):
    """righe di codice contententi il setup della terapia, necessario per poterla visualizzare"""
    setup.setTerapia(accounts[1],"Terapia X", {'from': accounts[6]})

    """questa riga di codice contiene un test che dovrebbe andare a buon fine, in quanto la richiesta di vedere una terapia di un paziente
    viene fatta dall'account del paziente a cui è assegnata la terapia, come dovrebbe essere"""
    assert setup.getTerapia(accounts[1], {'from':accounts[1]})

def test_get_terapia_ex1(setup):
    """righe di codice contententi il setup della terapia, necessario per poterla visualizzare"""
    setup.setTerapia(accounts[1],"Terapia X", {'from': accounts[6]})

    """questa riga di codice contiene un test che non dovrebbe andare a buon fine, in quanto la richiesta di vedere una terapia di un paziente
    viene fatta specificando un account paziente che non esiste. L'output aspettato sarebbe 'Paziente inesistente' """
    with pytest.raises(Exception):
        setup.getTerapia(accounts[7], {'from':accounts[1]})

def test_get_terapia_ex2(setup):
    """righe di codice contententi il setup della terapia, necessario per poterla visualizzare"""
    setup.setTerapia(accounts[1],"Terapia X", {'from': accounts[6]})

    """questa riga di codice contiene un test che non dovrebbe andare a buon fine, in quanto la richiesta di vedere una terapia di un paziente
    viene fatta da un account che non ha i permessi necessari. L'output aspettato sarebbe 'Utente non autorizzato!' """
    with pytest.raises(Exception):
        setup.getTerapia(accounts[1], {'from':accounts[7]})

def test_get_pazienti(setup):
    """questa riga di codice contiene un test che dovrebbe andare a buon fine, dato che la richiesta per vedere i pazienti
    avviene da un account ASUR, come dovrebbe essere"""
    assert setup.getPazienti({'from':accounts[0]})

def test_get_pazienti_ex(setup):
    """questa riga di codice contiene un test che non dovrebbe andare a buon fine, dato che la richiesta per vedere i pazienti
    avviene da un account non ASUR (paziente in questo caso). L'output aspettato sarebbe 'Utente senza privilegi necessari' """
    with pytest.raises(Exception):
        setup.getPazienti({'from':accounts[5]})

def test_get_richieste(setup):
    #Setup delle richieste necessario per vedere tutte le richieste presenti
    setup.SetRichieste(accounts[1], 0, 0, {'from': accounts[0]})

    """questa riga di codice contiene un test che dovrebbe andare a buon fine, dato che la richiesta per vedere le richieste
    avviene da un account ASUR, come dovrebbe essere"""
    assert setup.getRichieste({'from':accounts[0]})

def test_get_richieste_ex(setup):
    #Setup delle richieste necessario per vedere tutte le richieste presenti
    setup.SetRichieste(accounts[1], 0, 0, {'from': accounts[0]})
    
    """questa riga di codice contiene un test che dovrebbe andare a buon fine, dato che la richiesta per vedere le richieste
    avviene da un account non ASUR (paziente in questo caso), L'output aspettato sarebbe 'Utente senza privilegi necessari'"""
    with pytest.raises(Exception):
        assert setup.getRichieste({'from':accounts[1]})