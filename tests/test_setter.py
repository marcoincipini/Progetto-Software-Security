import brownie
import pytest
import scripts.setup as set
import scripts.pinata as pinata
from brownie import GestioneADI, accounts

# Funzione di setup che viene eseguita prima di ogni test
@pytest.fixture(scope="module", autouse=True)
def setup():
    # Deploy del contratto GestioneADI prima di ogni test
    contratto =  GestioneADI.deploy(accounts[0],{'from':accounts[0]})
    # setup degli utenti che servono per gestire gli account delle funzioni usate da questi test
    set.utenti(contratto)
    yield contratto

# Test per il metodo setTerapia
def test_set_terapia(setup):
    # togliere il commento alla tipologia di test che si desidera eseguire

    """questa riga di codice contiene un test che non dovrebbe andare a buon fine, dato che prova
    ad accedere alle terapie con un account che non è quello di un medico, dovrebbe dare come errore 'Medico inesistente' """
    #assert setup.setTerapia(accounts[1], "Terapia X", {'from': accounts[8]})

    """questa riga di codice contiene un test che non dovrebbe andare a buon fine, dato che l'account che prova a
    settare la terapia è un account medico, ma non è quello associato al paziente giusto, quindi dovrebbe restituire come errore
    'Medico non associato al paziente' """
    #assert setup.setTerapia(accounts[1], "Terapia X", {'from': accounts[7]})

    """queste righe di codice contengono un test che dovrebbe andare a buon fine, dato che prova
    ad accedere alle terapie con un account che è quello di un medico"""
    
    assert setup.setTerapia(accounts[1],"Terapia X", {'from': accounts[6]})


# Test per il metodo setPaziente
def test_set_paziente(setup):
    # togliere il commento alla tipologia di test che si desidera eseguire

    """queste righe di codice contengono un test che non dovrebbe andare a buon fine, dato che il set della struttura
    paziente dovrebbe essere fatto solamente da un account con livello di privilegio ASUR, invece in questo caso viene fatto
    da un account che dovrebbe essere quello di un medico"""
    assert setup.setPaziente(accounts[1], 0, 0, {'from': accounts[6]})
    
    """queste righe di codice contengono un test che dovrebbe andare a buon fine, dato che il set della struttura
    paziente viene fatto  da un account con livello di privilegio ASUR"""
    # assert setup.setPaziente(accounts[1], 0, 0, {'from': accounts[0]})


# Test per il metodo setPazienteASUR
def test_set_paziente_asur(setup):
    # togliere il commento alla tipologia di test che si desidera eseguire
    # Setup delle richieste necessario per lanciare il metodo setPazienteASUR
    setup.SetRichieste(accounts[1], 0, 0, {'from': accounts[0]})

    """queste righe di codice contengono un test che non dovrebbe andare a buon fine, dato che il set del paziente della struttura
    pazienteASUR dovrebbe essere fatto solamente da un account con livello di privilegio ASUR, invece in questo caso viene fatto
    da un account che dovrebbe essere quello di un medico"""
    # assert setup.setPazienteASUR(accounts[1], 0, 0, 0, {'from': accounts[6]})

    """queste righe di codice contengono un test che dovrebbe andare a buon fine, dato che il set della struttura
    pazienteASUR viene fatto  da un account con livello di privilegio ASUR"""
    assert setup.setPazienteASUR(accounts[1], 0, 0, 0, {'from': accounts[0]})