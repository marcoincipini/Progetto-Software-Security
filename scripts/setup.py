from brownie import accounts, network, Contract, GestioneADI

# Devo sempre definire un metodo main
def main():
    contratto=GestioneADI.deploy(accounts[0],{'from':accounts[0]})
    #contratto.setPaziente(accounts[1],10,10)
    return contratto
