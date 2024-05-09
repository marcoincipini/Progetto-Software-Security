#!/bin/bash

# Aggiorna i repository
sudo apt update
sudo apt upgrade

# Controlla se Python 3.11 è già installato
if python3.11 --version &>/dev/null; then
    echo "Python 3.11 è già installato."
else
    echo "Python 3.11 non è installato. Installazione in corso..."
    sudo apt install -y python3.11
    echo "Python 3.11 è stato installato con successo."
fi

# Controlla se PIP3 è già installato
if pip3 --version &>/dev/null; then
    echo "PIP3 è già installato."
else
    echo "PIP3 non è installato. Installazione in corso..."
    sudo apt install -y python3-pip
    echo "PIP3 è stato installato con successo."
fi

# Controlla se Node.js è già installato
if nodejs --version &>/dev/null; then
    echo "Node.js è già installato."
else
    echo "Node.js non è installato. Installazione in corso..."
    sudo apt install -y nodejs
    echo "Node.js è stato installato con successo."
fi

# Controlla se npm è già installato
if npm --version &>/dev/null; then
    echo "npm è già installato."
else
    echo "npm non è installato. Installazione in corso..."
    sudo apt install -y npm
    echo "npm è stato installato con successo."
fi

# Controlla se Git è già installato
if git --version &>/dev/null; then
    echo "Git è già installato."
else
    echo "Git non è installato. Installazione in corso..."
    sudo apt install -y git
    echo "Git è stato installato con successo."
fi

# Installa eth-brownie tramite pip3
pip3 install eth-brownie

# Installa ganache globalmente tramite npm
npm install -g ganache

# Clona il repository del progetto
git clone https://github.com/marcoincipini/Progetto-Software-Security.git

# Entra nella cartella del progetto
cd Progetto-Software-Security

# Compila il progetto con brownie
brownie compile
