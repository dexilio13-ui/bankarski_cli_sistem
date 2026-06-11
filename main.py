"""
main.py — Ulazna tačka bankarskog CLI sistema.
💭 Pokreće inicijalizaciju SQLite baze, zatim glavnu CLI petlju i prepušta kontrolu prezentacionom sloju.
"""
import sys
from repository.sqlite import init_db, seed_data
from cli.app import CLIApp

def main() -> None:
    """Inicijalizuje bazu i pokreće glavnu CLI aplikaciju."""
    try:
        # 💭 Faza 2: Inicijalizacija SQLite baze (kreiranje tabela ako ne postoje)
        init_db()
        seed_data()  # 💭 Dodato za automatsko popunjavanje

        # 💭 Pokretanje prezentacionog sloja koji dalje instancira servise
        app = CLIApp()
        app.run()
    except Exception as e:
        # ⚠️ Hvatanje neočekivanih kritičnih grešaka na nivou celog sistema
        print(f"Kritična greška sistema: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()