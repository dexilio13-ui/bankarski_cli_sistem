"""
models/enums.py — Definicije svih domenskih enumeracija.

💭 Zašto ovaj modul: Centralizacija statusa i tipova sprečava dupliranje logike
    i osigurava tipsku sigurnost širom aplikacije.
🔁 Odabir: StrEnum jer olakšava serijalizaciju u SQLite
    i čitljivost u CLI interfejsu.
    U kombinaciji sa StrEnum, funkcija auto() automatski dodeljuje malo ispisano ime samog člana.
"""

from enum import StrEnum, auto

class Uloga(StrEnum):
    """Nivoi privilegija u sistemu."""
    DIREKTOR = auto()
    RADNIK = auto()
    KLIJENT = auto()

class TipRacuna(StrEnum):
    """Vrste bankarskih računa."""
    TEKUCI = auto()
    STEDNI = auto()
    POSLOVNI = auto()

class Valuta(StrEnum):
    """Podržane valute u banci."""
    RSD = auto()
    EUR = auto()
    USD = auto()

class StatusRacuna(StrEnum):
    """Moguća stanja računa (State Pattern)."""
    AKTIVAN = auto()
    BLOKIRAN = auto()
    ZATVOREN = auto()

class TipTransakcije(StrEnum):
    """Tipovi finansijskih operacija."""
    UPLATA = auto()
    ISPLATA = auto()
    TRANSFER = auto()

class StatusTransakcije(StrEnum):
    """Ishod izvršenja transakcije."""
    USPESNA = auto()
    ODBIJENA = auto()
    NA_CEKANJU = auto()