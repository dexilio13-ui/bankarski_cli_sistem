"""
services/racun_service.py — Servis za upravljanje računima (uplata, isplata, transfer, status, otvaranje).
💭 Zašto ovaj modul: Centralizuje poslovnu logiku nad računima i osigurava
    da su operacije tip-sigurne, da pravilno rukovode greškama, beleže istoriju transakcija,
    poštuju restrikcije statusa računa (State pattern) i da se kreiranje vrši kroz Factory logiku.
"""

from typing import Optional, TYPE_CHECKING, Any
from uuid import UUID
from repository.interfaces import RacunRepo, TransakcijaRepo
from models.racun import Racun
from models.transakcija import Transakcija
from models.enums import StatusRacuna, TipRacuna, Valuta, TipTransakcije
from core.exceptions import NedovoljnoSredstavaError, StatusRacunaError

# Tip-only import za EventBus da bi mypy znao tip, bez runtime importa
if TYPE_CHECKING:
    pass  # type: ignore

# U runtimeu EventBus može, ali ne mora postojati; koristimo Optional[Any] za mypy
EventBusType = Optional[Any]


class RacunService:
    """Servis za poslovne operacije nad računima."""

    def __init__(
        self,
        racun_repo: RacunRepo,
        transakcija_repo: Optional[TransakcijaRepo] = None,
        event_bus: EventBusType = None,
    ) -> None:
        """Dependency Injection — repozitorijumi i opcionalni EventBus se ubacuju spolja."""
        self.racun_repo = racun_repo
        self.transakcija_repo = transakcija_repo
        self._event_bus = event_bus

    def _dohvati_racun_ili_baci(self, racun_id: UUID) -> Racun:
        """Pomoćna metoda koja dohvaća račun i baca ValueError ako ne postoji."""
        racun: Optional[Racun] = self.racun_repo.get_by_id(racun_id)
        if racun is None:
            raise ValueError(f"Račun sa ID {racun_id} ne postoji.")
        return racun

    def otvori_racun(self, vlasnik_id: UUID, tip: TipRacuna, valuta: Valuta) -> Racun:
        """Factory metoda koja kreira odgovarajući tip računa na osnovu parametra TipRacuna."""
        racun = Racun(vlasnik_id=vlasnik_id, tip=tip, valuta=valuta, stanje=0.0)

        # ⚠️ Direktno dodeljivanje specifičnih atributa u zavisnosti od tipa
        if tip == TipRacuna.STEDNI:
            racun.kamatna_stopa = 0.03
        elif tip == TipRacuna.POSLOVNI:
            racun.dozvoljeni_minus = 50_000.0

        self.racun_repo.save(racun)

        if self._event_bus is not None:
            try:
                self._event_bus.emit("racun_otvoren", racun=racun)
            except Exception:
                pass

        return racun

    def uplata(self, racun_id: UUID, iznos: float) -> None:
        """Dodaje sredstva na račun i beleži transakciju u istoriju."""
        racun = self._dohvati_racun_ili_baci(racun_id)

        # 🛡️ State Pattern: ZATVOREN račun blokira uplate (priliv)
        if racun.status == StatusRacuna.ZATVOREN:
            raise StatusRacunaError("Nije dozvoljena uplata na račun koji je ZATVOREN.")

        racun.stanje += iznos
        self.racun_repo.save(racun)

        # 📝 Beleženje transakcije u bazu
        if self.transakcija_repo is not None:
            nova_transakcija = Transakcija(
                racun_id=racun_id, iznos=iznos, tip=TipTransakcije.UPLATA
            )
            self.transakcija_repo.save(nova_transakcija)

        if self._event_bus is not None:
            self._event_bus.emit("uplata_izvrsena", racun=racun, iznos=iznos)

    def isplata(self, racun_id: UUID, iznos: float) -> None:
        """Skida sredstva sa računa; baci grešku ako nema sredstava ili ako je status restriktivan."""
        racun = self._dohvati_racun_ili_baci(racun_id)

        # 🛡️ State Pattern: BLOKIRAN i ZATVOREN račun ne dozvoljavaju isplate (odliv)
        if racun.status == StatusRacuna.BLOKIRAN:
            raise StatusRacunaError(
                "Nije dozvoljena isplata. Račun je trenutno BLOKIRAN."
            )
        if racun.status == StatusRacuna.ZATVOREN:
            raise StatusRacunaError("Nije dozvoljena isplata. Račun je ZATVOREN.")

        # 💭 Direktno dohvatamo polje, sa sigurnosnim fallbackom na 0.0 ako je None
        dozvoljeni_minus = racun.dozvoljeni_minus or 0.0
        limit = -dozvoljeni_minus

        if racun.stanje - iznos < limit:
            raise NedovoljnoSredstavaError("Nedovoljno sredstava na računu.")

        racun.stanje -= iznos
        self.racun_repo.save(racun)

        # 📝 Beleženje transakcije u bazu
        if self.transakcija_repo is not None:
            nova_transakcija = Transakcija(
                racun_id=racun_id, iznos=iznos, tip=TipTransakcije.ISPLATA
            )
            self.transakcija_repo.save(nova_transakcija)

        if self._event_bus is not None:
            self._event_bus.emit("isplata_izvrsena", racun=racun, iznos=iznos)

    def transfer(self, izvor_id: UUID, cilj_id: UUID, iznos: float) -> None:
        """Prenosi sredstva sa jednog računa na drugi uz striktne provere statusa."""
        izvor = self._dohvati_racun_ili_baci(izvor_id)
        cilj = self._dohvati_racun_ili_baci(cilj_id)

        # 🛡️ State Pattern: Izvor (odliv sredstava) ne sme biti BLOKIRAN ni ZATVOREN
        if izvor.status == StatusRacuna.BLOKIRAN:
            raise StatusRacunaError("Transfer nije moguć. Izvorni račun je BLOKIRAN.")
        if izvor.status == StatusRacuna.ZATVOREN:
            raise StatusRacunaError("Transfer nije moguć. Izvorni račun je ZATVOREN.")

        # 🛡️ State Pattern: Cilj (priliv sredstava) ne sme biti ZATVOREN (BLOKIRAN račun može primiti novac)
        if cilj.status == StatusRacuna.ZATVOREN:
            raise StatusRacunaError("Transfer nije moguć. Ciljni račun je ZATVOREN.")

        izvor_limit = -(izvor.dozvoljeni_minus or 0.0)
        if izvor.stanje - iznos < izvor_limit:
            raise NedovoljnoSredstavaError("Nedovoljno sredstava na izvornom računu.")

        izvor.stanje -= iznos
        cilj.stanje += iznos

        self.racun_repo.save(izvor)
        self.racun_repo.save(cilj)

        # 📝 Beleženje transakcije u bazu za oba računa
        if self.transakcija_repo is not None:
            transakcija_izvor = Transakcija(
                racun_id=izvor_id, iznos=iznos, tip=TipTransakcije.TRANSFER
            )
            transakcija_cilj = Transakcija(
                racun_id=cilj_id, iznos=iznos, tip=TipTransakcije.TRANSFER
            )
            self.transakcija_repo.save(transakcija_izvor)
            self.transakcija_repo.save(transakcija_cilj)

        if self._event_bus is not None:
            self._event_bus.emit(
                "transfer_izvrsen", izvor=izvor, cilj=cilj, iznos=iznos
            )

    def blokiraj_racun(self, racun_id: UUID) -> None:
        """Postavlja status računa na BLOKIRAN."""
        racun = self._dohvati_racun_ili_baci(racun_id)
        try:
            racun.promeni_status(StatusRacuna.BLOKIRAN)
            self.racun_repo.save(racun)
            if self._event_bus is not None:
                self._event_bus.emit("racun_blokiran", racun=racun)
        except ValueError as e:
            raise StatusRacunaError(str(e))

    def odblokiraj_racun(self, racun_id: UUID) -> None:
        """Vraća račun u AKTIVAN status."""
        racun = self._dohvati_racun_ili_baci(racun_id)
        try:
            racun.promeni_status(StatusRacuna.AKTIVAN)
            self.racun_repo.save(racun)
            if self._event_bus is not None:
                self._event_bus.emit("racun_odblokiran", racun=racun)
        except ValueError as e:
            raise StatusRacunaError(str(e))

    def zatvori_racun(self, racun_id: UUID) -> None:
        """Postavlja račun u ZATVOREN status."""
        racun = self._dohvati_racun_ili_baci(racun_id)
        try:
            racun.promeni_status(StatusRacuna.ZATVOREN)
            self.racun_repo.save(racun)
            if self._event_bus is not None:
                self._event_bus.emit("racun_zatvoren", racun=racun)
        except ValueError as e:
            raise StatusRacunaError(str(e))
