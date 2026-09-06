"""
cli/views.py — Zadužen isključivo za ispisivanje podataka na ekran.
💭 Odvajanjem prikaza od logike postižemo čist kod. Servisi vraćaju podatke,
    a views.py ih samo formatira i prikazuje.
🔁 Odabir: Rich (Console/Panel) — konzistentan, formatiran ispis svuda u CLI-ju.
"""

from rich.console import Console
from rich.panel import Panel

console = Console()


def prikazi_naslov(tekst: str) -> None:
    """Ispisuje formatiran naslov ekrana (Rich panel)."""
    console.print(
        Panel(
            f"[bold yellow]🏦 {tekst.upper()}[/bold yellow]",
            border_style="bright_blue",
            expand=False,
        )
    )


def prikazi_uspeh(poruka: str) -> None:
    """Ispisuje poruku o uspešnoj operaciji."""
    console.print(f"[bold green]✅ USPEH:[/bold green] {poruka}")


def prikazi_gresku(poruka: str) -> None:
    """Ispisuje poruku o grešci."""
    console.print(f"[bold red]❌ GREŠKA:[/bold red] {poruka}")


def prikazi_info(poruka: str) -> None:
    """Ispisuje informativnu poruku."""
    console.print(f"[bold cyan]ℹ️ INFO:[/bold cyan] {poruka}")


def prikazi_meni_opcije(opcije: dict[str, str]) -> None:
    """Ispisuje dostupne opcije iz prosleđenog rečnika (Rich panel)."""
    sadrzaj = "\n".join(
        f"[cyan][{kljuc}][/cyan] {opis}" for kljuc, opis in opcije.items()
    )
    console.print(
        Panel(sadrzaj, title="Izaberite opciju", border_style="dim", expand=False)
    )