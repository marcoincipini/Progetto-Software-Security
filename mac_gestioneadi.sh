#   

#!/bin/bash

# Install Homebrew if not already installed
if ! command -v brew &>/dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Set working directory
echo "Setting working directory..."
sudo mkdir -p ~/usr/app
sudo chown -R $(whoami) ~/usr/app
cd ~/usr/app

# Install Node.js using Homebrew
echo "Installing Node.js..."
brew install node

# Install Python 
echo "Installing Python 3.12.2"
brew install python

# Install Brownie
echo "Installing Brownie..."
pip install eth-brownie

# Install Ganache 
echo "Installing Ganache..."
npm install ganache --global

# Clone repository and compile with Brownie
echo "Cloning repository and compiling with Brownie..."
git clone https://github.com/marcoincipini/Progetto-Software-Security.git ~/usr/app/Progetto-Software-Security
cd ~/usr/app/Progetto-Software-Security
brownie compile
echo "Installation completed successfully!"
