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

    // Inserire tutti i require necessari

    // Setter di tutte le strutture
    function setPaziente(address _pz, uint8 _lat, uint8 _lon) public {
        pazienti.push(paziente(_pz, _lat, _lon));
    }

    function setMedico(address _medico) public{
        medici.push(_medico);
    }

    function setOperatore(address _operatore) public {
        operatori.push(_operatore);
    }

    function setAsur(address _asur) public{
        asur = _asur;
    }

    function setAttrezzatura(address _pz, string memory _att) public{
        ckattrezzatura.push(attrezzature(_pz, _att));
    }

    function setTerapia(address _pz, string memory _ter) public{
        ckterapie.push(terapie(_pz, _ter));
    }

    function SetConferma(address _pz, address _op, string memory _prest) public{
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
}
