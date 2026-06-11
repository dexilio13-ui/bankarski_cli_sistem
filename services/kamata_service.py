"""
services/kamata_service.py — Servis za obračun kamate.
💭 Zašto ovaj modul: Implementira Strategy pattern za različite algoritme obračuna kamate.
"""

from abc import ABC, abstractmethod
from models.racun import Racun


# -------------------------------
# Strategije obračuna kamate
# -------------------------------

class KamataStrategy(ABC):
    """Apstraktna strategija za obračun kamate."""

    @abstractmethod
    def obracunaj(self, racun: Racun, stopa: float, period: int) -> float:
        """
        Obračunava kamatu za dati račun.

        Args:
            racun (Racun): Račun na kojem se obračunava kamata.
            stopa (float): Godišnja kamatna stopa (npr. 0.05 = 5%).
            period (int): Period u godinama.

        Returns:
            float: Iznos kamate.
        """
        ...


class ProstaKamata(KamataStrategy):
    """Strategija za obračun proste kamate."""

    def obracunaj(self, racun: Racun, stopa: float, period: int) -> float:
        # Formula: K = P * r * t
        return racun.stanje * stopa * period


class SlozenaKamata(KamataStrategy):
    """Strategija za obračun složene kamate."""

    def obracunaj(self, racun: Racun, stopa: float, period: int) -> float:
        # Formula: K = P * (1 + r)^t - P
        return racun.stanje * ((1 + stopa) ** period - 1)


# -------------------------------
# Servis koji koristi strategije
# -------------------------------

class KamataService:
    """Servis za obračun kamate koristeći izabranu strategiju."""

    def __init__(self, strategy: KamataStrategy) -> None:
        """
        Dependency Injection — strategija se ubacuje spolja.
        Može biti ProstaKamata ili SlozenaKamata.
        """
        self.strategy = strategy

    def izracunaj_kamatu(self, racun: Racun, stopa: float, period: int) -> float:
        """Izračunava kamatu koristeći izabranu strategiju."""
        return self.strategy.obracunaj(racun, stopa, period)