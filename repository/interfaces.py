"""
repository/interfaces.py — Apstraktni interfejsi za perzistenciju.
💭 Zašto ovaj modul: Repository pattern omogućava da servisni sloj ne zna da li čitamo iz RAM-a ili SQLite-a.
"""

from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from models.korisnik import Korisnik
from models.racun import Racun
from models.transakcija import Transakcija


class KorisnikRepo(ABC):
    """Interfejs za operacije sa korisnicima."""

    @abstractmethod
    def get_by_id(self, korisnik_id: UUID) -> Optional[Korisnik]: ...

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[Korisnik]: ...

    @abstractmethod
    def get_all(self) -> List[Korisnik]: ...

    @abstractmethod
    def save(self, korisnik: Korisnik) -> None: ...


class RacunRepo(ABC):
    """Interfejs za operacije sa računima."""

    @abstractmethod
    def get_by_id(self, racun_id: UUID) -> Optional[Racun]: ...

    @abstractmethod
    def get_by_vlasnik(self, vlasnik_id: UUID) -> List[Racun]: ...

    @abstractmethod
    def get_all(self) -> List[Racun]: ...

    @abstractmethod
    def save(self, racun: Racun) -> None: ...


class TransakcijaRepo(ABC):
    """Interfejs za operacije sa transakcijama."""

    @abstractmethod
    def get_by_racun(self, racun_id: UUID) -> List[Transakcija]: ...

    @abstractmethod
    def save(self, transakcija: Transakcija) -> None: ...
