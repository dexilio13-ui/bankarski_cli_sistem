"""
main.py — Ulazna tačka bankarskog CLI sistema.
💭 Pokreće inicijalizaciju SQLite baze, zatim glavnu CLI petlju i prepušta kontrolu prezentacionom sloju.
"""

import os
import sys

from rich.console import Console

from cli.app import CLIApp
from repository.sqlite import init_db, seed_data

os.system("")  # Aktivira ANSI escape codes u Windows terminalu

console = Console(stderr=True)


def main() -> None:
    """Inicijalizuje bazu i pokreće glavnu CLI aplikaciju."""
    try:
        # 💭 Faza 2: Inicijalizacija SQLite baze (kreiranje tabela ako ne postoje)
        init_db()
        seed_data()  # 💭 Dodato za automatsko popunjavanje

        # 💭 Pokretanje prezentacionog sloja koji dalje instancira servise
        app = CLIApp()
        app.run()
    except Exception as e:  # noqa: BLE001 — namerno hvatamo sve kritične greške
        # ⚠️ Hvatanje neočekivanih kritičnih grešaka na nivou celog sistema
        console.print(f"[bold red]Kritična greška sistema:[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
