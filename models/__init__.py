"""
models/__init__.py — Inicijalizacija modula sa modelima.
"""

# Dodajemo __all__ kako bismo linteru rekli da su ovi importi tu sa razlogom (javni interfejs modula).
from .enums import (
    StatusRacuna,
    StatusTransakcije,
    TipRacuna,
    TipTransakcije,
    Uloga,
    Valuta,
)
from .korisnik import Direktor, Klijent, Korisnik, Radnik
from .racun import Racun
from .transakcija import Transakcija

__all__ = [
    "Direktor",
    "Klijent",
    "Korisnik",
    "Racun",
    "Radnik",
    "StatusRacuna",
    "StatusTransakcije",
    "TipRacuna",
    "TipTransakcije",
    "Transakcija",
    "Uloga",
    "Valuta",
]
