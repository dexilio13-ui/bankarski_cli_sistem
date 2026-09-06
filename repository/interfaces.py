"""
repository/interfaces.py — Apstraktni interfejsi za perzistenciju.
💭 Zašto ovaj modul: Repository pattern omogućava da servisni sloj ne zna da li čitamo iz RAM-a ili SQLite-a.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from models.korisnik import Korisnik
from models.racun import Racun
from models.transakcija import Transakcija


class KorisnikRepo(ABC):
    """Interfejs za operacije sa korisnicima."""

    @abstractmethod
    def get_by_id(self, korisnik_id: UUID) -> Korisnik | None: ...

    @abstractmethod
    def get_by_username(self, username: str) -> Korisnik | None: ...

    @abstractmethod
    def get_all(self) -> list[Korisnik]: ...

    @abstractmethod
    def save(self, korisnik: Korisnik) -> None: ...


class RacunRepo(ABC):
    """Interfejs za operacije sa računima."""

    @abstractmethod
    def get_by_id(self, racun_id: UUID) -> Racun | None: ...

    @abstractmethod
    def get_by_vlasnik(self, vlasnik_id: UUID) -> list[Racun]: ...

    @abstractmethod
    def get_all(self) -> list[Racun]: ...

    @abstractmethod
    def save(self, racun: Racun) -> None: ...


class TransakcijaRepo(ABC):
    """Interfejs za operacije sa transakcijama."""

    @abstractmethod
    def get_by_racun(self, racun_id: UUID) -> list[Transakcija]: ...

    @abstractmethod
    def save(self, transakcija: Transakcija) -> None: ...
