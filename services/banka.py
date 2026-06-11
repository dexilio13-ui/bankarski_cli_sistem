"""
services/banka.py — Centralna Banka klasa (Singleton).

💭 Zašto ovaj modul: Orkestrira poslovne operacije i delegira perzistenciju SQLite repozitorijumima u Fazi 2.
🔁 Odabir: Prelazak sa in-memory rečnika na SQLite repozitorijume uz očuvanje Singleton strukture.
"""

from typing import Any
from uuid import UUID
from models.racun import Racun
from models.transakcija import Transakcija
from models.enums import TipRacuna, Valuta
from repository.sqlite import SQLiteRacunRepo, SQLiteTransakcijaRepo


class SingletonMeta(type):
    """Metaklasa koja osigurava da postoji samo jedna banka.

    💭 Zašto ovaj pattern: Projektni zahtev izričito nalaže SingletonMeta.
    """

    _instances: dict[type, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Banka(metaclass=SingletonMeta):
    """Centralna banka redefinisana za rad sa SQLite perzistentnim slojem (Faza 2)."""

    def __init__(self) -> None:
        """Inicijalizuje SQLite repozitorijume za upravljanje podacima."""
        # 💭 U Fazi 2 menjamo in-memory rečnike namenskim SQLite repozitorijumima
        self.racun_repo = SQLiteRacunRepo()
        self.transakcija_repo = SQLiteTransakcijaRepo()

    def kreiraj_racun(self, vlasnik_id: UUID, tip: TipRacuna, valuta: Valuta) -> Racun:
        """Kreira novi račun i perzistira ga u bazu preko repozitorijuma.

        💭 Zašto ovaj pristup: Racun model vrši inicijalnu konfiguraciju preko svog konstruktora,
        a repo osigurava trajno čuvanje.
        """
        novi_racun = Racun(vlasnik_id=vlasnik_id, tip=tip, valuta=valuta)
        self.racun_repo.save(novi_racun)
        return novi_racun

    def izvrsi_transakciju(self, racun_id: UUID, iznos: float, tip: str) -> None:
        """Izvršava poslovnu logiku transakcije nad računom pronađenim u bazi.

        Raises:
            ValueError: Ako račun ne postoji u bazi podataka.
        """
        racun = self.racun_repo.get_by_id(racun_id)
        if not racun:
            raise ValueError(f"Račun sa ID {racun_id} ne postoji u sistemu.")

        self._azuriraj_stanje(racun, iznos, tip)
        self._evidentiraj(racun_id, iznos, tip)

    def _azuriraj_stanje(self, racun: Racun, iznos: float, tip: str) -> None:
        """Ažurira stanje objekta u memoriji i sinhronizuje promene sa bazom podataka.

        Nedovoljno sredstava na računu ili nepoznat tip transakcije baca grešku.
        """
        if tip == "UPLATA":
            racun.stanje += iznos
        elif tip == "ISPLATA" and racun.stanje >= iznos:
            racun.stanje -= iznos
        else:
            raise ValueError("Neispravna transakcija ili nedovoljno sredstava.")

        self.racun_repo.save(racun)

    def _evidentiraj(self, racun_id: UUID, iznos: float, tip: str) -> None:
        """Kreira novi zapis transakcije i trajno ga upisuje u bazu."""
        nova_transakcija = Transakcija(racun_id=racun_id, iznos=iznos, tip=tip)
        self.transakcija_repo.save(nova_transakcija)