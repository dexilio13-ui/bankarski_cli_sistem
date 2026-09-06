"""
migracija_lozinki.py — Jednokratna migracija postojećih lozinki na SHA-256 heš (Faza 3).

💭 Zašto ovaj fajl: Tvoja postojeća banka.db već ima korisnike sa lozinkama
    u čistom tekstu (Faza 1/2). Pošto proveri_lozinku() sada poredi SHA-256
    heš, prijava više ne bi radila za te korisnike bez ove migracije.
    Skript prepisuje password kolonu na heš, a sve ostalo (računi,
    transakcije, status...) ostaje netaknuto.

⚠️ VAŽNO:
    - Pokreni OVO TAČNO JEDNOM, nakon što ubaciš sve fajlove iz koraka
      "Hashovanje lozinki", a PRE narednog pokretanja main.py.
    - Skript prepoznaje već heširane lozinke (64 hex karaktera) i
      preskače ih, pa je bezbedan i ako ga greškom pokreneš dvaput.

Pokretanje (iz root foldera projekta, sa aktiviranim .venv):
    python migracija_lozinki.py
"""

import sqlite3
from pathlib import Path

from core.security import hesiraj_lozinku

DB_PATH = Path("banka.db")
DUZINA_SHA256_HEX = 64


def _izgleda_kao_hes(vrednost: str) -> bool:
    """Heuristika: SHA-256 heš je uvek 64 hex karaktera (0-9, a-f)."""
    if len(vrednost) != DUZINA_SHA256_HEX:
        return False

    hex_cifre = set("0123456789abcdef")
    return all(karakter in hex_cifre for karakter in vrednost)


def migriraj_lozinke() -> None:
    """Prepisuje sve plain-text lozinke u korisnici tabeli na SHA-256 heš."""
    if not DB_PATH.exists():
        print("❌ banka.db ne postoji — pokreni main.py prvo da se baza kreira.")
        return

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT id, username, password FROM korisnici")
        korisnici = cursor.fetchall()

        izmenjeno = 0
        preskoceno = 0

        for korisnik_id, username, lozinka in korisnici:
            if _izgleda_kao_hes(lozinka):
                preskoceno += 1
                continue

            novi_hes = hesiraj_lozinku(lozinka)
            conn.execute(
                "UPDATE korisnici SET password = ? WHERE id = ?",
                (novi_hes, korisnik_id),
            )
            print(f"  🔒 {username}: lozinka heširana.")
            izmenjeno += 1

    print(f"\n✅ Migracija završena — heširano: {izmenjeno}, preskočeno (već heširano): {preskoceno}.")


if __name__ == "__main__":
    migriraj_lozinke()
