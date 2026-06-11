"""
services/auth_service.py — Servis za autentifikaciju i upravljanje korisnicima.
💭 Zašto ovaj modul: Centralizuje biznis logiku prijave i osigurava postojanje inicijalnih naloga.
"""

from typing import List
from repository.interfaces import KorisnikRepo
from models.korisnik import Direktor, Radnik, Klijent, Korisnik
from core.exceptions import AutentifikacijaError


class AuthService:
    """Servis za autentifikaciju korisnika."""

    def __init__(self, korisnik_repo: KorisnikRepo) -> None:
        """💭 Dependency Injection omogućava laku zamenu skladišta (Memory -> SQLite)."""
        self.korisnik_repo = korisnik_repo

    def login(self, username: str, lozinka: str) -> Korisnik:
        """Prijava korisnika na osnovu korisničkog imena i lozinke."""
        korisnik = self.korisnik_repo.get_by_username(username)
        # ⚠️ Sigurnosna napomena: U produkciji lozinke nikada ne čuvati u plain-textu
        if korisnik is None or not korisnik.proveri_lozinku(lozinka):
            raise AutentifikacijaError("Neispravno korisničko ime ili lozinka.")
        return korisnik

    def seed_korisnici(self) -> None:
        """🔁 Refaktorisano: Razbijeno na manje celine zbog pravila od 15 linija."""
        korisnici = self._generisi_inicijalne_korisnike()
        for k in korisnici:
            self._snimi_ako_nedostaje(k)

    def _generisi_inicijalne_korisnike(self) -> List[Korisnik]:
        """Pomoćna metoda koja vraća listu podrazumevanih sistemskih korisnika."""
        return [
            Direktor(ime="Marko", prezime="Kraljević", username="admin", password="admin123"),
            Radnik(ime="Jovan", prezime="Jovanović", username="radnik1", password="pass1"),
            Radnik(ime="Ana", prezime="Anić", username="radnik2", password="pass2"),
            Klijent(ime="Pera", prezime="Perić", username="pera1", password="klijentpass1"),
        ]

    def _snimi_ako_nedostaje(self, korisnik: Korisnik) -> None:
        """⚠️ Proverava postojanje po username-u pre nego što upiše entitet u bazu."""
        existing = self.korisnik_repo.get_by_username(korisnik.username)
        if existing is None:
            self.korisnik_repo.save(korisnik)