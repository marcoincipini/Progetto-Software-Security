// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.4;

contract GestioneADI {
    // Attributi
    // Struttura informazioni del paziente (hash)
    struct paziente {
        address pz;
        uint8 lat;
        uint8 lon;
    }

    // Struttura informazioni attrezzature (hash)
    struct attrezzature {
        address paziente;
        string attrezzatura;
    }

    // Struttura informazioni terapie (hash)
    struct terapie {
        address paziente;
        string terapia;
    }

    // Struttura gestione delle conferme
    struct conferme {
        address paziente;
        address operatore;
        string prestazione;
        string id;
    }

    paziente[] private richieste;           // Array delle richieste ADI
    paziente[] private pazienti;            // Array dei pazienti
    address[] private medici;               // Array dei medici
    address[] private operatori;            // Array degli operatori sanitari
    address private asur;                   // Account amministratore
    attrezzature[] private listaattrezzatura;   // Array delle attrezzature (hash)
    terapie[] private listaterapie;         // Array delle terapie (1 per paziente) (hash)
    conferme[] private conferma;            // Array gestione delle conferme operatore
    conferme[] private validazione;         // Array gestione delle conferme paziente

    // Informazioni su chi può inserire prestazioni per un determinato paziente
    mapping(address => address) private medicoCurante; // Associazione paziente-medico (chiave-valore)

    // dalla versione 0.7.0 non è necessaria la specifica della visibilità nel costruttore
    constructor(address _asur) { 
        asur = _asur;
    }

    /**
    SETTER DI TUTTE LE STRUTTURE
     */
    function SetRichieste(address _pz, uint8 _lat, uint8 _lon) public {
        richieste.push(paziente(_pz, _lat, _lon));
    }
    
    function setPaziente(address _pz, uint8 _lat, uint8 _lon) public {
        require(msg.sender == asur, "Utente senza privilegi necessari");

        pazienti.push(paziente(_pz, _lat, _lon));
    }

    function setMedico(address _medico) public{
        require(msg.sender == asur, "Utente senza privilegi necessari");

        medici.push(_medico);
    }

    function setOperatore(address _operatore) public {
        require(msg.sender == asur, "Utente senza privilegi necessari");

        operatori.push(_operatore);
    }

    function setAttrezzatura(address _pz, string memory _att) public{
        require(msg.sender == asur, "Utente senza privilegi necessari");
        require(ckpaziente(_pz), "Paziente inesistente");

        listaattrezzatura.push(attrezzature(_pz, _att));
    }

    function setTerapia(address _pz, string memory _ter) public{
        require(ckmedico(msg.sender), "Medico inesistente");
        require(ckpaziente(_pz), "Paziente inesistente");
        require(medicoCurante[_pz]==msg.sender, "Medico non associato al paziente");

        listaterapie.push(terapie(_pz, _ter));
    }

    function setConferma(address _pz, address _op, string memory _prest, string memory _id) public{
        require(ckpaziente(_pz), "Paziente inesistente");
        require(ckmedico(_op)||ckoperatore(_op), "Medico inesistente");
        require(msg.sender == asur || medicoCurante[_pz]==msg.sender, "Utente senza privilegi necessari");

        conferma.push(conferme(_pz, _op, _prest, _id));
    }

    function confermaOperatore(uint256 _lat, uint256 _lon,  uint256 _i) public{
        conferme memory prestazione = conferma[_i];
        require(cklocpaziente(_lat, _lon, prestazione.paziente), "Operatore non localizzato");
        validazione.push(prestazione);
        delete conferma[_i];
    }

    // prestazione validata dal paziente
    function confermaPaziente(uint256 _i) public{
        require(_i < conferma.length, "indice inesistente!!");

        delete validazione[_i];
    }

    // Setter del mapping paziente-medico
    function setmedicoCurante(address _pz, address _md) public{
        require(ckpaziente(_pz), "Paziente inesistente");
        require(ckmedico(_md), "Medico inesistente");

        medicoCurante[_pz] = _md;
    }

    /**
    CONTROLLI SULLA PRESENZA DI VALORI NEGLI ARRAY
     */
    function ckpaziente(address _pz) private view returns (bool){
        for (uint256 i=0; i < pazienti.length; i++){
            if (pazienti[i].pz == _pz){return true;}
        }
        return false;
    }

    function cklocpaziente(uint256 _lat, uint256 _lon, address _pz) private view returns (bool){
        for (uint256 i=0; i < pazienti.length; i++){
            if (pazienti[i].pz == _pz){
                if ((pazienti[i].lat==_lat)||(pazienti[i].lon==_lon)){return true;}
                return false;
            }
        }
        return false;
    }

    function ckmedico(address _md) private view returns (bool){
        for (uint256 i=0; i < medici.length; i++){
            if (medici[i] == _md){return true;}
        }
        return false;
    }

    function ckoperatore(address _op) private view returns (bool){
        for (uint256 i=0; i < operatori.length; i++){
            if (operatori[i] == _op){return true;}
        }
        return false;
    }

    function ckattrezzature(address _pz) public view returns (string memory hashcode){
        require(ckpaziente(_pz), "Paziente inesistente");
        for (uint256 i=0; i < listaattrezzatura.length; i++){
            if(listaattrezzatura[i].paziente == _pz){
                return listaattrezzatura[i].attrezzatura;
            }

        }
    }

    function ckterapie(address _pz) public view returns (string memory hashcode){
        require(ckpaziente(_pz), "Paziente inesistente");
        for (uint256 i=0; i < listaterapie.length; i++){
            if(listaterapie[i].paziente == _pz){
                return listaterapie[i].terapia;
            }

        }
    }

    /**
    GETTER DELLE STRUTTURE DATI
     */
    function getTerapia(address _pz) public view returns (string memory hashcode){
        require(ckpaziente(_pz), "Paziente inesistente");
        require(msg.sender == _pz || msg.sender == medicoCurante[_pz], "Utente non autorizzato!");
        return ckterapie(_pz);
    }

    function getConfermeall() public view returns (conferme[] memory){
        require(msg.sender == asur, "Utente senza privilegi necessari");
        return conferma;
    }

    function getConferme() public view returns (conferme[] memory) {
        require(ckoperatore(msg.sender), "Utente senza privilegi necessari");
        
        // Creare un array dinamico temporaneo per memorizzare le conferme
        conferme[] memory confOpTemp = new conferme[](conferma.length);
        uint256 count = 0;

        // Iterare attraverso l'array di conferme
        for (uint256 i = 0; i < conferma.length; i++) {
            // Se l'operatore corrente è l'utente chiamante, aggiungi la conferma all'array temporaneo
            if (conferma[i].operatore == msg.sender) {
                confOpTemp[count] = conferma[i];
                count++;
            }
        }

        // Creare un nuovo array dinamico della dimensione corretta
        conferme[] memory confOp = new conferme[](count);
        
        // Copiare gli elementi dall'array temporaneo al nuovo array di output
        for (uint256 j = 0; j < count; j++) {
            confOp[j] = confOpTemp[j];
        }

        return confOp;
    }

    function getValidazione() public view returns (conferme[] memory){
        require(ckpaziente(msg.sender), "Utente senza privilegi necessari");
        
        // Creare un array dinamico temporaneo per memorizzare le conferme
        conferme[] memory confOpTemp = new conferme[](validazione.length);
        uint256 count = 0;

        // Iterare attraverso l'array di conferme
        for (uint256 i = 0; i < validazione.length; i++) {
            // Se l'operatore corrente è l'utente chiamante, aggiungi la conferma all'array temporaneo
            if (validazione[i].operatore == msg.sender) {
                confOpTemp[count] = validazione[i];
                count++;
            }
        }

        // Creare un nuovo array dinamico della dimensione corretta
        conferme[] memory confOp = new conferme[](count);
        
        // Copiare gli elementi dall'array temporaneo al nuovo array di output
        for (uint256 j = 0; j < count; j++) {
            confOp[j] = confOpTemp[j];
        }

        return confOp;
    }
}
