"""
models/__init__.py — Inicijalizacija modula sa modelima.
"""

# Dodajemo __all__ kako bismo linteru rekli da su ovi importi tu sa razlogom (javni interfejs modula).
from .korisnik import Korisnik, Direktor, Radnik, Klijent
from .racun import Racun
from .transakcija import Transakcija
from .enums import (
    Uloga,
    TipRacuna,
    Valuta,
    StatusRacuna,
    TipTransakcije,
    StatusTransakcije,
)

__all__ = [
    "Korisnik",
    "Direktor",
    "Radnik",
    "Klijent",
    "Racun",
    "Transakcija",
    "Uloga",
    "TipRacuna",
    "Valuta",
    "StatusRacuna",
    "TipTransakcije",
    "StatusTransakcije",
]
