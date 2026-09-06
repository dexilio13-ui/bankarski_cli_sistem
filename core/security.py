"""
core/security.py — Heširanje i provera lozinki (Faza 3).

💭 Zašto ovaj modul: Centralizuje logiku heširanja tako da lozinke
    nikada ne budu sačuvane kao čist tekst u bazi podataka.
🔁 Odabir: hashlib.sha256 — ugrađena, jednosmerna heš funkcija;
    projektna specifikacija eksplicitno traži hashlib.sha256
    umesto čuvanja čistog teksta.
"""

import hashlib


def hesiraj_lozinku(lozinka: str) -> str:
    """Vraća SHA-256 heš lozinke u hex formatu.

    Args:
        lozinka: Lozinka u čistom tekstu (npr. unesena pri registraciji).

    Returns:
        64-karakterni hex string — SHA-256 heš lozinke.
    """
    return hashlib.sha256(lozinka.encode("utf-8")).hexdigest()


def lozinka_je_ispravna(lozinka: str, hes: str) -> bool:
    """Poredi unetu lozinku (čist tekst) sa sačuvanim SHA-256 hešom.

    Args:
        lozinka: Lozinka koju korisnik unosi prilikom prijave.
        hes: Heš sačuvan u bazi (rezultat funkcije hesiraj_lozinku).

    Returns:
        True ako heš unete lozinke odgovara sačuvanom hešu.
    """
    return hesiraj_lozinku(lozinka) == hes
