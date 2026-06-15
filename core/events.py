"""
core/events.py — EventBus implementacija (Observer pattern).

💭 Zašto ovaj modul: Omogućava da se različiti delovi sistema pretplate na događaje
    i budu obavešteni kada se oni dese.
"""

from typing import Callable, Dict, List


class EventBus:
    """Jednostavan EventBus za registraciju i emitovanje događaja."""

    def __init__(self) -> None:
        # Dict gde je ključ ime događaja, a vrednost lista callback funkcija
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable) -> None:
        """
        Dodaje pretplatu na događaj.
        Args:
            event_name (str): Ime događaja (npr. "racun_otvoren").
            callback (Callable): Funkcija koja će se pozvati kada se događaj desi.
        """
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(callback)

    def emit(self, event_name: str, *args, **kwargs) -> None:
        """
        Emituje događaj i poziva sve pretplaćene callback funkcije.
        Args:
            event_name (str): Ime događaja.
            *args, **kwargs: Parametri koji se prosleđuju callback funkcijama.
        """
        for callback in self._subscribers.get(event_name, []):
            callback(*args, **kwargs)


# ENTRY POINT TEST

if __name__ == "__main__":
    bus = EventBus()

    # Definišemo callback funkcije
    def log_event(racun_id, iznos):
        print(f"[LOG] Transakcija na računu {racun_id}, iznos: {iznos}")

    def notify_event(racun_id, iznos):
        print(
            f"[NOTIFY] Klijentu šaljemo obaveštenje o transakciji {iznos} na računu {racun_id}"
        )

    # Pretplaćujemo se na događaj "transakcija_izvršena"
    bus.subscribe("transakcija_izvršena", log_event)
    bus.subscribe("transakcija_izvršena", notify_event)

    # Emitujemo događaj
    bus.emit("transakcija_izvršena", racun_id="123-456", iznos=500)
