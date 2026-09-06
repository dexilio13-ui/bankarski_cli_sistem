"""
services/auth_service.py — Servis za autentifikaciju i upravljanje korisnicima.
💭 Zašto ovaj modul: Centralizuje biznis logiku prijave i osigurava postojanje inicijalnih naloga.
"""


from core.exceptions import AutentifikacijaError
from core.security import hesiraj_lozinku
from models.korisnik import Direktor, Klijent, Korisnik, Radnik
from repository.interfaces import KorisnikRepo


class AuthService:
    """Servis za autentifikaciju korisnika."""

    def __init__(self, korisnik_repo: KorisnikRepo) -> None:
        """💭 Dependency Injection omogućava laku zamenu skladišta (Memory -> SQLite)."""
        self.korisnik_repo = korisnik_repo

    def login(self, username: str, lozinka: str) -> Korisnik:
        """Prijava korisnika na osnovu korisničkog imena i lozinke."""
        korisnik = self.korisnik_repo.get_by_username(username)
        # 💭 Faza 3: proveri_lozinku() sada poredi SHA-256 heš, ne čist tekst.
        if korisnik is None or not korisnik.proveri_lozinku(lozinka):
            raise AutentifikacijaError("Neispravno korisničko ime ili lozinka.")
        return korisnik

    def seed_korisnici(self) -> None:
        """🔁 Refaktorisano: Razbijeno na manje celine zbog pravila od 15 linija.

        ⚠️ Napomena: Ova metoda se trenutno ne poziva iz main.py — seed_data()
            u repository/sqlite.py je aktivni mehanizam punjenja baze.
            Ostavljena radi konzistentnosti API-ja i mogućeg budućeg korišćenja.
        """
        korisnici = self._generisi_inicijalne_korisnike()
        for k in korisnici:
            self._snimi_ako_nedostaje(k)

    def _generisi_inicijalne_korisnike(self) -> list[Korisnik]:
        """Pomoćna metoda koja vraća listu podrazumevanih sistemskih korisnika."""
        return [
            Direktor(ime="Marko", prezime="Kraljević", username="admin", password=hesiraj_lozinku("admin123")),
            Radnik(ime="Jovan", prezime="Jovanović", username="radnik1", password=hesiraj_lozinku("pass1")),
            Radnik(ime="Ana", prezime="Anić", username="radnik2", password=hesiraj_lozinku("pass2")),
            Klijent(ime="Pera", prezime="Perić", username="pera1", password=hesiraj_lozinku("klijentpass1")),
        ]

    def _snimi_ako_nedostaje(self, korisnik: Korisnik) -> None:
        """⚠️ Proverava postojanje po username-u pre nego što upiše entitet u bazu."""
        existing = self.korisnik_repo.get_by_username(korisnik.username)
        if existing is None:
            self.korisnik_repo.save(korisnik)
