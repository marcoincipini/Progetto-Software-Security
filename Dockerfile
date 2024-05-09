# Questo Dockerfile configura un ambiente Python con Node.js utilizzando nvm.
# Installa anche eth-brownie, ganache e compila un progetto.

# Utilizza l'immagine ufficiale di Python 3.11.9 come base.
FROM python:3.11.9-bullseye

# Aggiorna il gestore dei pacchetti.
RUN apt update

# Imposta le variabili d'ambiente per nvm.
ENV NVMDIR /root/.nvm/
ENV NODE_VERSION 20.12.2

# Scarica e installa nvm.
RUN curl https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh -o install.sh
RUN chmod +x install.sh
RUN ./install.sh

# Installa la versione specificata di Node.js.
RUN /bin/bash --login -c "nvm install ${NODE_VERSION}"
ENV NODE_PATH $NVMDIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVMDIR/versions/node/v$NODE_VERSION/bin/:$PATH

# Verifica la versione di Node.js installata.
RUN node -v

# Imposta la directory di lavoro.
WORKDIR /usr/app

# Installa eth-brownie tramite pip.
RUN pip3 install eth-brownie

# Aggiorna nuovamente il gestore dei pacchetti.
RUN apt update

# Installa ganache globalmente tramite npm.
RUN npm install ganache --global

# Clona il repository GitHub specificato.
RUN git clone https://github.com/marcoincipini/Progetto-Software-Security.git

# Imposta la directory di lavoro sul progetto clonato.
WORKDIR /usr/app/Progetto-Software-Security

# Compila il progetto utilizzando brownie.
RUN brownie compile

# Imposta il comando predefinito per eseguire /bin/sh.
CMD ["/bin/sh"]
