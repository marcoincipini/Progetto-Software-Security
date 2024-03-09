// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.4;

contract GestioneADI {
    // Attributi
    struct paziente {
        address pz;
        uint8 lat;
        uint8 lon;
    }

    struct attrezzature {
        address paziente;
        string attrezzatura; // Valutare se possibile bytes32
    }

    struct terapie {
        address paziente;
        string terapia; // Valutare se possibile bytes32
    }

    struct conferme {
        address paziente;
        address operatore;
        string prestazione;
    }

    paziente[] private pazienti;
    address[] private medici;
    address[] private operatori;
    address private asur;
    attrezzature[] private ckattrezzatura;
    terapie[] private ckterapie;
    conferme[] private conferma;

    mapping(address => address) private medicoBase;

    // Inserire tutti i require necessari
    // Creare una funzione che controlli se un elemento è presente nell'array

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

    function removeConferma(uint256 _i) public{
        require(_i < conferma.length, "indice inesistente!!");

        delete conferma[_i];
    }

    function setMedicobase(address _pz, address _md) public{
        require(_pz, "Paziente inesistente");
        require(_md, "Medico inesistente");

        medicoBase[_pz] = _md;
    }
}
