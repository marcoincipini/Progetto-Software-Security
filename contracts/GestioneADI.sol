// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.4;

contract GestioneADI {
    // Attributi
    // Struttura informazioni del paziente (hash)
    struct Paziente {
        address pz;
        uint8 lat;
        uint8 lon;
    }

    // Struttura informazioni attrezzature (hash)
    struct Attrezzature {
        address paziente;
        bytes32 attrezzatura;
    }

    // Struttura informazioni terapie (hash)
    struct Terapie {
        address paziente;
        string terapia;
    }

    // Struttura gestione delle conferme
    struct Conferme {
        address paziente;
        address operatore;
        string prestazione;
        string id;
    }

    Paziente[] private richieste; // Array delle richieste ADI
    Paziente[] private pazienti; // Array dei pazienti
    address[] private medici; // Array dei medici
    address[] private operatori; // Array degli operatori sanitari
    address private asur; // Account amministratore
    Attrezzature[] private listaattrezzatura; // Array delle attrezzature (hash)
    Terapie[] private listaterapie; // Array delle terapie (1 per paziente) (hash)
    Conferme[] private conferma; // Array gestione delle conferme operatore
    Conferme[] private validazione; // Array gestione delle conferme paziente

    // Informazioni su chi può inserire prestazioni per un determinato paziente
    mapping(address => address) private medicoCurante; // Associazione paziente-medico (chiave-valore)

    // dalla versione 0.7.0 non è necessaria la specifica della visibilità nel costruttore
    constructor(address _asur) {
        asur = _asur;
    }

    // modifier che controlla che l'utente sia ASUR
    modifier onlyASUR() {
        require(msg.sender == asur, "Utente senza privilegi necessari");
        _;
    }

    // modifier che controlla l'esistenza di un paziente
    modifier checkEsistenzaPz(address _pz) {
        require(ckpaziente(_pz), "Paziente inesistente");
        _;
    }

    /**
    SETTER DI TUTTE LE STRUTTURE
     */
    function setRichieste(address _pz, uint8 _lat, uint8 _lon) public {
        richieste.push(Paziente(_pz, _lat, _lon));
    }

    function setPaziente(address _pz, uint8 _lat, uint8 _lon) public onlyASUR {
        pazienti.push(Paziente(_pz, _lat, _lon));
    }

    // setter per un paziente che viene inserito attraverso una sua richiesta ADI
    function setPazienteASUR(
        address _pz,
        uint8 _lat,
        uint8 _lon,
        uint8 _index
    ) public onlyASUR {
        setPaziente(_pz, _lat, _lon);

        for (uint i = _index; i < richieste.length - 1; i++) {
            richieste[i] = richieste[i + 1];
        }
        richieste.pop();
    }

    function setMedico(address _medico) public onlyASUR {
        medici.push(_medico);
    }

    function setOperatore(address _operatore) public onlyASUR {
        operatori.push(_operatore);
    }

    function setAttrezzatura(
        address _pz,
        uint256 _id,
        string memory _att
    ) public onlyASUR checkEsistenzaPz(_pz) {
        bytes32 _hash = keccak256(abi.encode(_pz, _id, _att));
        listaattrezzatura.push(Attrezzature(_pz, _hash));
    }

    function setTerapia(
        address _pz,
        string memory _ter
    ) public checkEsistenzaPz(_pz) {
        require(ckmedico(msg.sender), "Medico inesistente");
        require(
            medicoCurante[_pz] == msg.sender,
            "Medico non associato al paziente"
        );
        // se è presente, elimino la terapia precedente
        for (uint i = 0; i < listaterapie.length; i++) {
            if (listaterapie[i].paziente == _pz) {
                delete listaterapie[i];
            }
        }
        listaterapie.push(Terapie(_pz, _ter));
    }

    function setConferma(
        address _pz,
        address _op,
        string memory _prest,
        string memory _id
    ) public checkEsistenzaPz(_pz) {
        require(ckmedico(_op) || ckoperatore(_op), "Medico inesistente");
        require(
            msg.sender == asur || medicoCurante[_pz] == msg.sender,
            "Utente senza privilegi necessari"
        );

        conferma.push(Conferme(_pz, _op, _prest, _id));
    }

    function confermaOperatore(
        uint256 _lat,
        uint256 _lon,
        string memory _id
    ) public {
        require(
            ckoperatore(msg.sender) || ckmedico(msg.sender),
            "Account non operatore!"
        );
        Conferme memory prestazione;
        uint256 indice = 0;
        bool flag = false;
        for (uint256 i = 0; i < conferma.length; i++) {
            if (
                keccak256(abi.encodePacked(conferma[i].id)) ==
                keccak256(abi.encodePacked(_id))
            ) {
                indice = i;
                prestazione = conferma[i];
                require(
                    msg.sender == prestazione.operatore,
                    "Operatore non autorizzato!"
                );
                flag = true;
            }
        }
        require(msg.sender == prestazione.operatore, "ID inesistente!");
        require(
            cklocpaziente(_lat, _lon, prestazione.paziente),
            "Operatore non localizzato!"
        );
        require(flag, "ID inesistente");
        validazione.push(prestazione);
        for (uint256 index = indice; index < conferma.length - 1; index++) {
            conferma[index] = conferma[index + 1];
        }
        conferma.pop();
    }

    // prestazione validata dal paziente
    function confermaPaziente(string memory _id) public {
        require(ckpaziente(msg.sender), "Account non paziente");
        Conferme memory prestazione;
        uint256 indice = 0;
        bool flag = false;
        for (uint256 i = 0; i < validazione.length; i++) {
            if (
                keccak256(abi.encodePacked(validazione[i].id)) ==
                keccak256(abi.encodePacked(_id))
            ) {
                indice = i;
                prestazione = validazione[i];
                flag = true;
            }
        }
        require(msg.sender == prestazione.paziente, "ID inesistente!");
        require(flag, "ID inesistente");
        for (uint256 index = indice; index < validazione.length - 1; index++) {
            validazione[index] = validazione[index + 1];
        }
        validazione.pop();
    }

    // Setter del mapping paziente-medico
    function setmedicoCurante(
        address _pz,
        address _md
    ) public checkEsistenzaPz(_pz) {
        require(ckmedico(_md), "Medico inesistente");

        medicoCurante[_pz] = _md;
    }

    /**
    CONTROLLI SULLA PRESENZA DI VALORI NEGLI ARRAY
     */
    function ckpaziente(address _pz) private view returns (bool) {
        for (uint256 i = 0; i < pazienti.length; i++) {
            if (pazienti[i].pz == _pz) {
                return true;
            }
        }
        return false;
    }

    function cklocpaziente(
        uint256 _lat,
        uint256 _lon,
        address _pz
    ) private view returns (bool) {
        for (uint256 i = 0; i < pazienti.length; i++) {
            if (pazienti[i].pz == _pz) {
                if ((pazienti[i].lat == _lat) && (pazienti[i].lon == _lon)) {
                    return true;
                }
                return false;
            }
        }
        return false;
    }

    function ckmedico(address _md) private view returns (bool) {
        for (uint256 i = 0; i < medici.length; i++) {
            if (medici[i] == _md) {
                return true;
            }
        }
        return false;
    }

    function ckoperatore(address _op) private view returns (bool) {
        for (uint256 i = 0; i < operatori.length; i++) {
            if (operatori[i] == _op) {
                return true;
            }
        }
        return false;
    }

    function ckattrezzature(
        address _pz
    ) public view checkEsistenzaPz(_pz) returns (bytes32 hashcode) {
        for (uint256 i = 0; i < listaattrezzatura.length; i++) {
            if (listaattrezzatura[i].paziente == _pz) {
                return listaattrezzatura[i].attrezzatura;
            }
        }
    }

    function ckterapie(
        address _pz
    ) public view checkEsistenzaPz(_pz) returns (string memory hashcode) {
        for (uint256 i = 0; i < listaterapie.length; i++) {
            if (listaterapie[i].paziente == _pz) {
                return listaterapie[i].terapia;
            }
        }
    }

    /**
    GETTER DELLE STRUTTURE DATI
     */

    function getRichieste() public view onlyASUR returns (Paziente[] memory) {
        return richieste;
    }

    function getTerapia(
        address _pz
    ) public view checkEsistenzaPz(_pz) returns (string memory hashcode) {
        require(
            msg.sender == _pz || msg.sender == medicoCurante[_pz],
            "Utente non autorizzato!"
        );
        return ckterapie(_pz);
    }

    function getConfermeall() public view onlyASUR returns (Conferme[] memory) {
        return conferma;
    }

    function getConferme() public view returns (Conferme[] memory) {
        require(ckoperatore(msg.sender), "Utente senza privilegi necessari");

        // Crea un array dinamico temporaneo per memorizzare le conferme
        Conferme[] memory confOpTemp = new Conferme[](conferma.length);
        uint256 count = 0;

        // Itera le conferme
        for (uint256 i = 0; i < conferma.length; i++) {
            // Se l'operatore corrente è l'utente chiamante, aggiunge la conferma all'array temporaneo
            if (conferma[i].operatore == msg.sender) {
                confOpTemp[count] = conferma[i];
                count++;
            }
        }

        // Crea un nuovo array dinamico della dimensione corretta
        Conferme[] memory confOp = new Conferme[](count);

        // Copia gli elementi dall'array temporaneo al nuovo array di output
        for (uint256 j = 0; j < count; j++) {
            confOp[j] = confOpTemp[j];
        }

        return confOp;
    }

    function getValidazione() public view returns (Conferme[] memory) {
        require(ckpaziente(msg.sender), "Utente senza privilegi necessari");

        Conferme[] memory confOpTemp = new Conferme[](validazione.length);
        uint256 count = 0;

        for (uint256 i = 0; i < validazione.length; i++) {
            if (validazione[i].paziente == msg.sender) {
                confOpTemp[count] = validazione[i];
                count++;
            }
        }

        Conferme[] memory confOp = new Conferme[](count);
        for (uint256 j = 0; j < count; j++) {
            confOp[j] = confOpTemp[j];
        }

        return confOp;
    }

    function getMedici() public view onlyASUR returns (address[] memory) {
        return medici;
    }

    // ritorna gli indirizzi di tutti i pazienti associati ad un medico
    function getPazientiDelMedico() public view returns (address[] memory) {
        require(ckmedico(msg.sender), "Utente non medico");
        address[] memory pazientiAssociatiTemp = new address[](pazienti.length);
        uint256 count = 0;
        for (uint256 i = 0; i < pazienti.length; i++) {
            if (medicoCurante[pazienti[i].pz] == msg.sender) {
                pazientiAssociatiTemp[count] = pazienti[i].pz;
                count++;
            }
        }

        address[] memory pazientiAssociati = new address[](count);
        for (uint256 j = 0; j < count; j++) {
            pazientiAssociati[j] = pazientiAssociatiTemp[j];
        }
        return pazientiAssociati;
    }

    function getPazienti() public view onlyASUR returns (Paziente[] memory) {
        return pazienti;
    }

    /**
    Validazione dei dati stream
     */

    function validaRilevazione(
        address _pz,
        uint256 _id,
        string memory _att
    ) public view checkEsistenzaPz(_pz) returns (bool) {
        require(msg.sender == _pz, "Paziente non autorizzato");
        return (keccak256(abi.encode(_pz, _id, _att)) == ckattrezzature(_pz));
    }
}
