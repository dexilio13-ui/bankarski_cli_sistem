import sys
from uuid import UUID
from rich.console import Console
from rich.table import Table

from core.exceptions import AutentifikacijaError
from repository.sqlite import SQLiteKorisnikRepo, SQLiteRacunRepo, SQLiteTransakcijaRepo
from services.auth_service import AuthService
from services.racun_service import RacunService
from models.korisnik import Korisnik, Klijent
from models.enums import Uloga, TipRacuna, Valuta
from cli import views, menus


console = Console(force_terminal=True, force_jupyter=False, color_system="256")

class CLIApp:
    def __init__(self) -> None:
        self.repo_korisnici = SQLiteKorisnikRepo()
        self.repo_racuni = SQLiteRacunRepo()
        self.repo_transakcije = SQLiteTransakcijaRepo()
        self.auth_svc = AuthService(self.repo_korisnici)
        self.racun_svc = RacunService(self.repo_racuni, self.repo_transakcije)
        self.trenutni_korisnik: Korisnik | None = None

    def run(self) -> None:
        views.prikazi_naslov("Bankarski CLI Sistem")
        while True:
            try:
                self._glavna_petlja()
            except (KeyboardInterrupt, SystemExit):
                console.print(
                    "\n[bold green]Hvala na korišćenju aplikacije![/bold green]"
                )
                break
            except Exception as e:
                views.prikazi_gresku(f"Neočekivana greška: {e}")

    def _glavna_petlja(self) -> None:
        if self.trenutni_korisnik is None:
            views.prikazi_meni_opcije(menus.GLAVNI_MENI)
            self._obradi_glavni_meni(input(">>> ").strip())
        else:
            self._rutiraj_po_ulozi()

    def _obradi_glavni_meni(self, izbor: str) -> None:
        if izbor == "0":
            sys.exit(0)
        elif izbor == "1":
            self._obradi_prijavu()
        else:
            views.prikazi_gresku("Nepoznata komanda.")

    def _obradi_prijavu(self) -> None:
        username = input("Korisničko ime: ").strip()
        lozinka = input("Lozinka: ").strip()
        try:
            self.trenutni_korisnik = self.auth_svc.login(username, lozinka)
            views.prikazi_uspeh(
                f"Prijavljeni ste kao {self.trenutni_korisnik.uloga.value}"
            )
        except AutentifikacijaError as e:
            views.prikazi_gresku(str(e))

    def _rutiraj_po_ulozi(self) -> None:
        if not self.trenutni_korisnik:
            return

        uloga = self.trenutni_korisnik.uloga
        if uloga == Uloga.DIREKTOR:
            views.prikazi_meni_opcije(menus.DIREKTOR_MENI)
            self._obradi_direktor_meni(input(">>> ").strip())
        elif uloga == Uloga.RADNIK:
            views.prikazi_meni_opcije(menus.RADNIK_MENI)
            self._obradi_radnik_meni(input(">>> ").strip())
        elif uloga == Uloga.KLIJENT:
            views.prikazi_meni_opcije(menus.KLIJENT_MENI)
            self._obradi_klijent_meni(input(">>> ").strip())

    def _obradi_radnik_meni(self, izbor: str) -> None:
        if izbor == "0":
            self.trenutni_korisnik = None
            views.prikazi_uspeh("Odjavljeni ste.")
        elif izbor == "1":
            self._radnik_otvori_racun()
        elif izbor == "2":
            self._radnik_blokiraj_racun()
        elif izbor == "3":
            self._radnik_registruj_klijenta()
        elif izbor == "4":
            self._radnik_odblokiraj_racun()
        elif izbor == "5":
            self._radnik_pregled_svih()
        else:
            views.prikazi_gresku("Nepoznata komanda.")

    def _radnik_otvori_racun(self) -> None:
        try:
            v_id = UUID(input("ID klijenta: ").strip())
            tip_mapa = {
                "tekuci": TipRacuna.TEKUCI,
                "stedni": TipRacuna.STEDNI,
                "poslovni": TipRacuna.POSLOVNI,
            }
            val_mapa = {"rsd": Valuta.RSD, "eur": Valuta.EUR, "usd": Valuta.USD}

            tip_str = input("Tip (tekuci/stedni/poslovni): ").strip().lower()
            val_str = input("Valuta (rsd/eur/usd): ").strip().lower()

            if tip_str not in tip_mapa or val_str not in val_mapa:
                raise ValueError("Pogrešan tip računa ili valuta.")

            r = self.racun_svc.otvori_racun(v_id, tip_mapa[tip_str], val_mapa[val_str])
            views.prikazi_uspeh(f"Uspešno otvoren račun: {r.id}")
        except Exception as e:
            views.prikazi_gresku(f"Greška: {e}")

    def _radnik_registruj_klijenta(self) -> None:
        try:
            ime = input("Ime klijenta: ").strip()
            prezime = input("Prezime klijenta: ").strip()
            username = input("Korisničko ime: ").strip()
            lozinka = input("Lozinka: ").strip()

            if not ime or not prezime or not username or not lozinka:
                raise ValueError("Sva polja su obavezna.")

            if self.repo_korisnici.get_by_username(username) is not None:
                raise ValueError(f"Korisničko ime '{username}' je već zauzeto.")

            novi_klijent = Klijent(ime=ime, prezime=prezime, username=username, password=lozinka)
            self.repo_korisnici.save(novi_klijent)
            views.prikazi_uspeh(f"Klijent registrovan! ID: {novi_klijent.id}")
        except Exception as e:
            views.prikazi_gresku(f"Greška: {e}")

    def _radnik_blokiraj_racun(self) -> None:
        try:
            racun_id = UUID(input("ID računa za blokiranje: ").strip())
            self.racun_svc.blokiraj_racun(racun_id)
            views.prikazi_uspeh("Račun je uspešno blokiran.")
        except Exception as e:
            views.prikazi_gresku(f"Greška: {e}")

    def _radnik_odblokiraj_racun(self) -> None:
        try:
            racun_id = UUID(input("ID računa za odblokiranje: ").strip())
            self.racun_svc.odblokiraj_racun(racun_id)
            views.prikazi_uspeh("Račun je uspešno odblokiran.")
        except Exception as e:
            views.prikazi_gresku(f"Greška: {e}")

    def _radnik_pregled_svih(self) -> None:
        korisnici = [
            k for k in self.repo_korisnici.get_all() if k.uloga == Uloga.KLIJENT
        ]
        if not korisnici:
            console.print("[yellow]Nema registrovanih klijenata.[/yellow]")
            return

        table = Table(title="👥 Klijenti i njihovi računi", header_style="bold blue")
        table.add_column("Ime i prezime", style="bold")
        table.add_column("Korisničko ime")
        table.add_column("Pripadajući računi (ID i Stanje)")

        for k in korisnici:
            racuni = self.repo_racuni.get_by_vlasnik(k.id)
            ako_nema = "Nema otvorenih računa"
            racuni_str = "\n".join(
                [
                    f"{r.tip.value}: {r.stanje:.2f} {r.valuta.value} ({r.id})"
                    for r in racuni
                ]
            )
            table.add_row(
                f"{k.ime} {k.prezime}", k.username, racuni_str if racuni else ako_nema
            )

        console.print(table)

    def _obradi_direktor_meni(self, izbor: str) -> None:
        if izbor == "0":
            self.trenutni_korisnik = None
            views.prikazi_uspeh("Odjavljeni ste.")
        elif izbor == "1":
            self._direktor_pregled_svih_racuna()
        elif izbor == "2":
            self._direktor_pregled_svih_transakcija()
        elif izbor == "3":
            self._direktor_blokiraj_racun()
        elif izbor == "4":
            self._direktor_pregled_klijenata()
        elif izbor == "5":
            self._direktor_odblokiraj_racun()
        elif izbor == "6":
            self._direktor_izvestaj_valute()
        else:
            views.prikazi_gresku("Nepoznata komanda.")

    def _direktor_pregled_svih_racuna(self) -> None:
        racuni = self.repo_racuni.get_all()
        if not racuni:
            console.print("[yellow]Nema registrovanih računa u banci.[/yellow]")
            return

        table = Table(title="🏦 Svi računi u banci", header_style="bold magenta")
        table.add_column("Račun ID", style="dim", width=36)
        table.add_column("Vlasnik")
        table.add_column("Tip računa")
        table.add_column("Stanje", justify="right", style="green")
        table.add_column("Status")

        for r in racuni:
            vlasnik = self.repo_korisnici.get_by_id(r.vlasnik_id)
            v_ime = f"{vlasnik.ime} {vlasnik.prezime}" if vlasnik else "Nepoznato"
            status_val = r.status.value if hasattr(r.status, "value") else str(r.status)
            status_style = (
                "[green]AKTIVAN[/green]"
                if "aktiv" in status_val.lower()
                else f"[red]{status_val}[/red]"
            )

            table.add_row(
                str(r.id),
                v_ime,
                r.tip.value if hasattr(r.tip, "value") else str(r.tip),
                f"{r.stanje:.2f} {r.valuta.value if hasattr(r.valuta, 'value') else str(r.valuta)}",
                status_style,
            )
        console.print(table)

    def _direktor_pregled_svih_transakcija(self) -> None:
        table = Table(title="📊 Sve transakcije u banci", header_style="bold cyan")
        table.add_column("Datum i vreme", style="dim")
        table.add_column("Račun ID", style="dim", width=36)
        table.add_column("Tip transakcije")
        table.add_column("Iznos", justify="right")

        ima_transakcija = False
        for r in self.repo_racuni.get_all():
            for t in self.repo_transakcije.get_by_racun(r.id):
                ima_transakcija = True
                tip_val = t.tip.value if hasattr(t.tip, "value") else str(t.tip)
                iznos_style = (
                    f"[green]+{t.iznos:.2f}[/green]"
                    if "uplata" in tip_val.lower()
                    else f"[red]-{t.iznos:.2f}[/red]"
                )
                valuta_str = (
                    r.valuta.value if hasattr(r.valuta, "value") else str(r.valuta)
                )
                table.add_row(
                    str(t.timestamp)[:19],
                    str(r.id),
                    tip_val,
                    f"{iznos_style} {valuta_str}",
                )

        if not ima_transakcija:
            console.print("[yellow]Nema zabeleženih transakcija u banci.[/yellow]")
        else:
            console.print(table)

    def _direktor_blokiraj_racun(self) -> None:
        try:
            racun_id = UUID(input("ID računa za blokiranje: ").strip())
            self.racun_svc.blokiraj_racun(racun_id)
            views.prikazi_uspeh("Račun je uspešno blokiran.")
        except Exception as e:
            views.prikazi_gresku(f"Greška: {e}")

    def _direktor_odblokiraj_racun(self) -> None:
        try:
            racun_id = UUID(input("ID računa za odblokiranje: ").strip())
            self.racun_svc.odblokiraj_racun(racun_id)
            views.prikazi_uspeh("Račun je uspešno odblokiran.")
        except Exception as e:
            views.prikazi_gresku(f"Greška: {e}")

    def _direktor_pregled_klijenata(self) -> None:
        korisnici = [
            k for k in self.repo_korisnici.get_all() if k.uloga == Uloga.KLIJENT
        ]
        if not korisnici:
            console.print("[yellow]Nema registrovanih klijenata u sistemu.[/yellow]")
            return

        table = Table(title="👥 Registar klijenata banke", header_style="bold blue")
        table.add_column("Klijent ID", style="dim", width=36)
        table.add_column("Ime i prezime")
        table.add_column("Korisničko ime")

        for k in korisnici:
            table.add_row(str(k.id), f"{k.ime} {k.prezime}", k.username)
        console.print(table)

    def _direktor_izvestaj_valute(self) -> None:
        izvestaj: dict[str, float] = {}
        for r in self.repo_racuni.get_all():
            val = r.valuta.value if hasattr(r.valuta, "value") else str(r.valuta)
            izvestaj[val] = izvestaj.get(val, 0.0) + r.stanje

        table = Table(title="💰 Ukupno stanje po valutama", header_style="bold yellow")
        table.add_column("Valuta")
        table.add_column("Ukupan Saldo", justify="right", style="bold green")
        for valuta, ukupno in izvestaj.items():
            table.add_row(valuta, f"{ukupno:,.2f}")
        console.print(table)

    def _obradi_klijent_meni(self, izbor: str) -> None:
        if izbor == "0":
            self.trenutni_korisnik = None
            views.prikazi_uspeh("Odjavljeni ste.")
        elif izbor == "1":
            self._klijent_pregled_racuna()
        elif izbor == "2":
            self._klijent_uplata()
        elif izbor == "3":
            self._klijent_isplata()
        elif izbor == "4":
            self._klijent_transfer()
        elif izbor == "5":
            self._klijent_istorija()
        else:
            views.prikazi_gresku("Nepoznata komanda.")

    def _klijent_pregled_racuna(self) -> None:
        if not self.trenutni_korisnik:
            return

        racuni = self.repo_racuni.get_by_vlasnik(self.trenutni_korisnik.id)
        if not racuni:
            console.print("[yellow]Nemate otvorenih računa.[/yellow]")
            return

        table = Table(title="🏦 Vaši računi", header_style="bold magenta")
        table.add_column("ID računa", style="dim", width=36)
        table.add_column("Tip računa")
        table.add_column("Stanje", justify="right", style="green")
        table.add_column("Status")

        for r in racuni:
            status_val = r.status.value if hasattr(r.status, "value") else str(r.status)
            status_style = (
                "[green]AKTIVAN[/green]"
                if "aktiv" in status_val.lower()
                else f"[red]{status_val}[/red]"
            )
            table.add_row(
                str(r.id),
                r.tip.value if hasattr(r.tip, "value") else str(r.tip),
                f"{r.stanje:.2f} {r.valuta.value if hasattr(r.valuta, 'value') else str(r.valuta)}",
                status_style,
            )
        console.print(table)

    def _klijent_uplata(self) -> None:
        if not self.trenutni_korisnik:
            return
        try:
            racuni = self.repo_racuni.get_by_vlasnik(self.trenutni_korisnik.id)
            if not racuni:
                console.print("[yellow]Nemate otvorenih računa.[/yellow]")
                return
            racun_id = UUID(input("ID računa: ").strip())
            if not any(r.id == racun_id for r in racuni):
                raise ValueError("Račun ne pripada vašem nalogu.")
            iznos = float(input("Iznos uplate: ").strip())
            if iznos <= 0:
                raise ValueError("Iznos mora biti veći od nule.")
            self.racun_svc.uplata(racun_id, iznos)
            views.prikazi_uspeh(f"Uplata od {iznos:.2f} uspešno izvršena.")
        except Exception as e:
            views.prikazi_gresku(f"Greška: {e}")

    def _klijent_isplata(self) -> None:
        if not self.trenutni_korisnik:
            return
        try:
            racuni = self.repo_racuni.get_by_vlasnik(self.trenutni_korisnik.id)
            if not racuni:
                console.print("[yellow]Nemate otvorenih računa.[/yellow]")
                return
            racun_id = UUID(input("ID računa: ").strip())
            if not any(r.id == racun_id for r in racuni):
                raise ValueError("Račun ne pripada vašem nalogu.")
            iznos = float(input("Iznos isplate: ").strip())
            if iznos <= 0:
                raise ValueError("Iznos mora biti veći od nule.")
            self.racun_svc.isplata(racun_id, iznos)
            views.prikazi_uspeh(f"Isplata od {iznos:.2f} uspešno izvršena.")
        except Exception as e:
            views.prikazi_gresku(f"Greška: {e}")

    def _klijent_transfer(self) -> None:
        if not self.trenutni_korisnik:
            return
        try:
            racuni = self.repo_racuni.get_by_vlasnik(self.trenutni_korisnik.id)
            if len(racuni) < 2:
                console.print("[yellow]Potrebna su najmanje dva računa za transfer.[/yellow]")
                return
            izvor_id = UUID(input("ID izvornog računa: ").strip())
            cilj_id = UUID(input("ID ciljnog računa: ").strip())
            if not any(r.id == izvor_id for r in racuni):
                raise ValueError("Izvorni račun ne pripada vašem nalogu.")
            if not any(r.id == cilj_id for r in racuni):
                raise ValueError("Ciljni račun ne pripada vašem nalogu.")
            iznos = float(input("Iznos transfera: ").strip())
            if iznos <= 0:
                raise ValueError("Iznos mora biti veći od nule.")
            self.racun_svc.transfer(izvor_id, cilj_id, iznos)
            views.prikazi_uspeh(f"Transfer od {iznos:.2f} uspešno izvršen.")
        except Exception as e:
            views.prikazi_gresku(f"Greška: {e}")

    def _klijent_istorija(self) -> None:
        if not self.trenutni_korisnik:
            return

        racuni = self.repo_racuni.get_by_vlasnik(self.trenutni_korisnik.id)
        if not racuni:
            console.print("[yellow]Nemate računa.[/yellow]")
            return

        for r in racuni:
            transakcije = self.repo_transakcije.get_by_racun(r.id)
            tip_racuna_str = r.tip.value if hasattr(r.tip, "value") else str(r.tip)
            valuta_str = r.valuta.value if hasattr(r.valuta, "value") else str(r.valuta)

            table = Table(
                title=f"📜 Transakcije za račun ({tip_racuna_str}):\n{r.id}",
                header_style="bold yellow",
            )
            table.add_column("Datum", style="dim")
            table.add_column("Tip transakcije")
            table.add_column("Iznos", justify="right")

            if not transakcije:
                table.add_row("N/A", "Nema transakcija", "0.00")
            else:
                for t in transakcije:
                    tip_val = t.tip.value if hasattr(t.tip, "value") else str(t.tip)
                    iznos_style = (
                        f"[green]+{t.iznos:.2f}[/green]"
                        if "uplata" in tip_val.lower()
                        else f"[red]-{t.iznos:.2f}[/red]"
                    )
                    table.add_row(
                        str(t.timestamp)[:16], tip_val, f"{iznos_style} {valuta_str}"
                    )

            console.print(table)
