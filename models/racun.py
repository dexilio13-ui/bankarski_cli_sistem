"""
models/racun.py — Model računa sa ispravljenim State pattern-om (ClassVar).

💭 Zašto ovaj modul: Centralizuje logiku stanja računa
🔁 Odabir:  ClassVar za isključivanje iz dataclass polja

"""

from dataclasses import dataclass, field
from typing import ClassVar
from uuid import uuid4, UUID

from models.enums import TipRacuna, Valuta, StatusRacuna

@dataclass
class Racun:
    """Predstavlja bankovni račun klijenta.

    💭 Zašto dataclass: Automatsko generisanje init, repr i eq metoda.
    🔁 Odabir: typing.ClassVar osigurava da dataclass ignoriše atribut.

    Attributes:
        vlasnik_id: UUID vlasnika računa
        tip: Tip računa (Tekući, Štedni, Poslovni)
        valuta: Valuta računa
        stanje: Trenutno stanje sredstava
        status: Status (Aktivan, Blokiran, Zatvoren)
        id: Jedinstveni identifikator
    """

    # 💭 Zašto ClassVar: Izričito govori dataclass-u da ovo NIJE instance polje i da ga ne parsira.
    _TRANZICIJE: ClassVar[dict[StatusRacuna, list[StatusRacuna]]] = {
        StatusRacuna.AKTIVAN: [StatusRacuna.BLOKIRAN, StatusRacuna.ZATVOREN],
        StatusRacuna.BLOKIRAN: [StatusRacuna.AKTIVAN, StatusRacuna.ZATVOREN],
        StatusRacuna.ZATVOREN: []
    }

    vlasnik_id: UUID
    tip: TipRacuna
    valuta: Valuta
    stanje: float = 0.0
    status: StatusRacuna = StatusRacuna.AKTIVAN
    id: UUID = field(default_factory=uuid4)
    kamatna_stopa: float | None = None  # Dodato za štedne račune
    dozvoljeni_minus: float | None = None  # Dodato za poslovne račune

    def promeni_status(self, novi_status: StatusRacuna) -> None:
        """Menja status računa ako je prelaz dozvoljen.

        💭 Zašto ovaj pristup: Korišćenje klasnog atributa za validaciju State patterna

        Args:
            novi_status (StatusRacuna): Željeno novo stanje računa.

        Returns:
            None: Mutira stanje objekta in-place.

        Raises:
            ValueError: Ako je prelaz nedozvoljen.


            - Pokušaj prelaza iz ZATVOREN u bilo šta drugo baca grešku.
        """
        # Provera da li je prelaz dozvoljen prema tranzicionoj mapi
        dozvoljeni = self._TRANZICIJE.get(self.status, [])
        if novi_status not in dozvoljeni:
            raise ValueError(f"Nedozvoljen prelaz iz {self.status.value} u {novi_status.value}")

        self.status = novi_status