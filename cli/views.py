"""
cli/views.py — Zadužen isključivo za ispisivanje podataka na ekran.
💭 Odvajanjem prikaza od logike postižemo čist kod. Servisi vraćaju podatke,
    a views.py ih samo formatira i prikazuje.
"""


def prikazi_naslov(tekst: str) -> None:
    """Ispisuje formatiran naslov ekrana."""
    print(f"\n{'=' * 40}")
    print(f"🏦 {tekst.upper()}")
    print(f"{'=' * 40}")


def prikazi_uspeh(poruka: str) -> None:
    """Ispisuje poruku o uspešnoj operaciji."""
    print(f"✅ USPEH: {poruka}")


def prikazi_gresku(poruka: str) -> None:
    """Ispisuje poruku o grešci."""
    print(f"❌ GREŠKA: {poruka}")


def prikazi_info(poruka: str) -> None:
    """Ispisuje informativnu poruku."""
    print(f"ℹ️ INFO: {poruka}")


def prikazi_meni_opcije(opcije: dict[str, str]) -> None:
    """Ispisuje dostupne opcije iz prosleđenog rečnika."""
    print("\nIzaberite opciju:")
    for kljuc, opis in opcije.items():
        print(f"  [{kljuc}] {opis}")
    print("-" * 40)
