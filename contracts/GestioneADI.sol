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
        string attrezzatura; // Valutare se possibile bytes32
    }

    // Struttura informazioni terapie (hash)
    struct terapie {
        address paziente;
        string terapia; // Valutare se possibile bytes32
    }

    // Struttura gestione delle conferme
    struct conferme {
        address paziente;
        address operatore;
        string prestazione;
    }

    paziente[] private pazienti;            // Array dei pazienti
    address[] private medici;               // Array dei medici
    address[] private operatori;            // Array degli operatori sanitari
    address private asur;                   // Account amministratore
    attrezzature[] private ckattrezzatura;  // Array delle attrezzature (hash)
    terapie[] private ckterapie;            // Array delle terapie (1 per paziente) (hash)
    conferme[] private conferma;            // Array gestione delle conferme

    // Informazioni su chi può inserire prestazioni per un determinato paziente
    mapping(address => address) private medicoBase; // Associazione paziente-medico (chiave-valore)

    // dalla versione 0.7.0 non è necessaria la specifica della visibilità nel costruttore
    constructor(address _asur) { 
        asur = _asur;
    }

    // Setter di tutte le strutture
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

        ckattrezzatura.push(attrezzature(_pz, _att));
    }

    function setTerapia(address _pz, string memory _ter) public{
        require(ckmedico(msg.sender), "Medico inesistente");
        require(ckpaziente(_pz), "Paziente inesistente");
        require(medicoBase[_pz]==msg.sender, "Medico non associato al paziente");

        ckterapie.push(terapie(_pz, _ter));
    }

    function SetConferma(address _pz, address _op, string memory _prest) public{ // Da completare
        require(ckpaziente(_pz), "Paziente inesistente");
        require(ckmedico(_op)||ckoperatore(_op), "Medico inesistente");

        conferma.push(conferme(_pz, _op, _prest));
    }

    // Remove della conferma (prestazione validata dal paziente)
    function removeConferma(uint256 _i) public{
        require(_i < conferma.length, "indice inesistente!!");

        delete conferma[_i];
    }

    // Setter del mapping paziente-medico
    function setMedicobase(address _pz, address _md) public{
        require(ckpaziente(_pz), "Paziente inesistente");
        require(ckmedico(_md), "Medico inesistente");

        medicoBase[_pz] = _md;
    }

    // Controlli sulla presenza di un valore negli array
    function ckpaziente(address _pz) private view returns (bool){
        for (uint256 i=0; i < pazienti.length; i++){
            if (pazienti[i].pz == _pz){return true;}
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
}
