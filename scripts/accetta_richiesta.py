from brownie import accounts, network, Contract, GestioneADI
import scripts.setup as set

#demo: l'ASUR visualizza e può confermare la richiesta di un paziente al programma ADI
def main():
    contratto=GestioneADI.deploy(accounts[0],{'from':accounts[0]})
    