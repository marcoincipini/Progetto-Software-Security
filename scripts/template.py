from brownie import accounts, network, Contract, GestioneADI

# Devo sempre definire un metodo main
def main():
    print(network.show_active())
    for i in accounts:
        print(i)
    t=GestioneADI.deploy(accounts[0],{'from':accounts[0]})
    t.setPaziente(accounts[1],10,10)
    print(t.getConferme())

