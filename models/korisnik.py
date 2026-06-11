"""models/korisnik.py — Model korisnika i specijalizovane role.

💭 Zašto ovaj modul: Centralizuje identifikaciju i autorizaciju korisnika u skladu sa arhitekturom.
🔁 Odabir: Pristup sa Dataclass sa init=False za role
"""

from dataclasses import dataclass, field
from uuid import uuid4, UUID
from models.enums import Uloga

@dataclass
class Korisnik:
    """Bazna klasa za sve korisnike sistema.

    💭 Zašto: Sadrži zajedničke atribute.
    """
    ime: str
    prezime: str
    username: str
    password: str
    uloga: Uloga
    id: UUID = field(default_factory=uuid4)

    def proveri_lozinku(self, lozinka: str) -> bool:
        # 💭 Zašto: U fazi 1 plain-text, u fazi 3 zamijeniti sa hash validacijom.
        return self.password == lozinka

@dataclass
class Direktor(Korisnik):
    """Direktor sa punim pristupom sistemu."""
    # 💭 Zašto: init=False sprječava prosljeđivanje uloge pri kreiranju objekta.
    uloga: Uloga = field(init=False, default=Uloga.DIREKTOR)

@dataclass
class Radnik(Korisnik):
    """Radnik sa ovlašćenjima za klijente i račune."""
    uloga: Uloga = field(init=False, default=Uloga.RADNIK)

@dataclass
class Klijent(Korisnik):
    """Klijent sa pristupom isključivo sopstvenim računima."""
    uloga: Uloga = field(init=False, default=Uloga.KLIJENT)