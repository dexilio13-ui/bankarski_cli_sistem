# repository/memory.py
"""
repository/memory.py — In-memory implementacija repozitorijuma.

💭 Zašto ovaj modul: Služi kao privremeni storage za Fazu 1 projekta.
🔁 Odabir: Instance klasa) za maksimalnu fleksibilnost i DI podršku.
"""

from uuid import UUID
from typing import List, Optional
from models.korisnik import Korisnik
from models.racun import Racun
from models.transakcija import Transakcija
from repository.interfaces import KorisnikRepo, RacunRepo, TransakcijaRepo


class MemoryKorisnikRepo(KorisnikRepo):
    """In-memory repozitorijum za korisnike."""

    def __init__(self) -> None:
        self._storage: dict[UUID, Korisnik] = {}

    def get_by_id(self, korisnik_id: UUID) -> Optional[Korisnik]:
        return self._storage.get(korisnik_id)

    def get_by_username(self, username: str) -> Optional[Korisnik]:
        #  iteriramo kroz dict za pronalazak po username
        for k in self._storage.values():
            if k.username == username:
                return k
        return None

    def save(self, korisnik: Korisnik) -> None:
        self._storage[korisnik.id] = korisnik


class MemoryRacunRepo(RacunRepo):
    """In-memory repozitorijum za račune."""

    def __init__(self) -> None:
        self._storage: dict[UUID, Racun] = {}

    def get_by_id(self, racun_id: UUID) -> Optional[Racun]:
        return self._storage.get(racun_id)

    def get_by_vlasnik(self, vlasnik_id: UUID) -> List[Racun]:
        # 💭 Zašto list comprehension: efikasno filtriranje
        return [r for r in self._storage.values() if r.vlasnik_id == vlasnik_id]

    def save(self, racun: Racun) -> None:
        self._storage[racun.id] = racun


class MemoryTransakcijaRepo(TransakcijaRepo):
    """In-memory repozitorijum za transakcije."""

    def __init__(self) -> None:
        self._storage: List[Transakcija] = []

    def get_by_racun(self, racun_id: UUID) -> List[Transakcija]:
        return [t for t in self._storage if t.racun_id == racun_id]

    def save(self, transakcija: Transakcija) -> None:
        self._storage.append(transakcija)
