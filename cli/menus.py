"""
cli/menus.py — Definicije menija za različite uloge u sistemu.
💭 Smeštanje menija u rečnike omogućava nam da prosledimo ove podatke
    funkciji `prikazi_meni_opcije` iz views.py bez prljanja glavne logike.
"""

GLAVNI_MENI = {
    "1": "Prijava na sistem",
    "0": "Izlaz iz aplikacije"
}

KLIJENT_MENI = {
    "1": "Pregled računa i stanja",
    "2": "Uplata na sopstveni račun",
    "3": "Isplata sa sopstvenog računa",
    "4": "Transfer između sopstvenih računa",
    "5": "Pregled istorije transakcija",
    "0": "Odjava"
}

RADNIK_MENI = {
    "1": "Otvaranje računa klijentu",
    "2": "Blokiranje računa",
    "3": "Registracija novog klijenta",
    "4": "Odblokiranje računa",
    "5": "Pregled klijenata i njihovih računa",
    "0": "Odjava"
}

DIREKTOR_MENI = {
    "1": "Pregled svih računa u banci",
    "2": "Pregled svih transakcija",
    "3": "Blokiranje računa",
    "4": "Pregled liste svih klijenata",
    "5": "Odblokiranje računa",
    "6": "Izveštaj o ukupnom stanju banke (po valutama)",
    "0": "Odjava"
}