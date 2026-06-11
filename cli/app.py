"""
cli/app.py — Glavni CLI kontroler i prezentacioni ruter.
💭 Zašto ovaj modul: Orkestrira korisnički unos, povezuje servise sa SQLite slojem.
"""

import sys
from uuid import UUID
from core.exceptions import AutentifikacijaError
from repository.sqlite import SQLiteKorisnikRepo, SQLiteRacunRepo, SQLiteTransakcijaRepo
from services.auth_service import AuthService
from services.racun_service import RacunService
from models.korisnik import Korisnik, Klijent
from models.enums import Uloga, TipRacuna, Valuta
from cli import views, menus


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
                print("\nHvala na korišćenju aplikacije!")
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
            views.prikazi_uspeh(f"Prijavljeni ste kao {self.trenutni_korisnik.uloga.value}")
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

    def _promena_lozinke(self) -> None:
        if not self.trenutni_korisnik:
            return
        nova = input("Unesite novu lozinku: ").strip()
        if len(nova) < 4:
            return views.prikazi_gresku("Lozinka mora imati bar 4 karaktera.")
        self.trenutni_korisnik.password = nova
        self.repo_korisnici.save(self.trenutni_korisnik)
        views.prikazi_uspeh("Lozinka uspešno promenjena.")

    # ==========================================
    # KLIJENT MENI LOGIKA
    # ==========================================

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
        elif izbor == "6":
            self._promena_lozinke()
        else:
            views.prikazi_gresku("Nepoznata opcija.")

    def _klijent_pregled_racuna(self) -> None:
        if not self.trenutni_korisnik: return
        racuni = self.repo_racuni.get_by_vlasnik(self.trenutni_korisnik.id)
        if not racuni:
            print("Nemate otvorenih računa.")
        for r in racuni:
            print(f"ID: {r.id} | Tip: {r.tip.value} | Stanje: {r.stanje:.2f} {r.valuta.value} | Status: {r.status.value}")

    def _klijent_uplata(self) -> None:
        try:
            r_id = UUID(input("Unesite ID računa: ").strip())
            iznos = float(input("Iznos uplate: ").strip())
            self.racun_svc.uplata(r_id, iznos)
            views.prikazi_uspeh("Uplata uspešno izvršena.")
        except Exception as e:
            views.prikazi_gresku(f"Greška: {e}")

    def _klijent_isplata(self) -> None:
        try:
            r_id = UUID(input("Unesite ID računa: ").strip())
            iznos = float(input("Iznos isplate: ").strip())
            self.racun_svc.isplata(r_id, iznos)
            views.prikazi_uspeh("Isplata uspešno izvršena.")
        except Exception as e:
            views.prikazi_gresku(f"Greška: {e}")

    def _klijent_transfer(self) -> None:
        try:
            izvor = UUID(input("ID izvornog računa: ").strip())
            cilj = UUID(input("ID ciljnog računa: ").strip())
            iznos = float(input("Iznos transfera: ").strip())
            self.racun_svc.transfer(izvor, cilj, iznos)
            views.prikazi_uspeh("Transfer uspešno izvršen.")
        except Exception as e:
            views.prikazi_gresku(f"Greška: {e}")

    def _klijent_istorija(self) -> None:
        if not self.trenutni_korisnik: return
        racuni = self.repo_racuni.get_by_vlasnik(self.trenutni_korisnik.id)
        for r in racuni:
            print(f"\nTransakcije za račun {r.id} ({r.tip.value}):")
            transakcije = self.repo_transakcije.get_by_racun(r.id)
            if not transakcije:
                print("  Nema registrovanih transakcija.")
            for t in transakcije:
                print(f"  [{t.timestamp}] {t.tip} | {t.iznos:.2f} {r.valuta.value}")

    # ==========================================
    # RADNIK MENI LOGIKA
    # ==========================================

    def _obradi_radnik_meni(self, izbor: str) -> None:
        if izbor == "0":
            self.trenutni_korisnik = None
            views.prikazi_uspeh("Odjavljeni ste.")
        elif izbor == "1":
            self._radnik_otvori_racun()
        elif izbor == "2":
            self._zajednicka_promena_statusa()  # Blokiranje
        elif izbor == "3":
            self._radnik_registruj_klijenta()   # Usklađeno sa Opcijom 3 (Registracija klijenta)
        elif izbor == "4":
            self._zajednicka_promena_statusa()  # Usklađeno sa Opcijom 4 (Odblokiranje računa)
        elif izbor == "5":
            self._radnik_pregled_svih()
        else:
            views.prikazi_gresku("Nepoznata opcija.")

    def _radnik_otvori_racun(self) -> None:
        try:
            v_id = UUID(input("ID klijenta: ").strip())

            # Mapiranje unosa u Enum vrednosti
            unos_tip = input("Tip (tekuci/stedni/poslovni): ").strip().lower()
            mapa_tipova = {
                "tekuci": TipRacuna.TEKUCI,
                "stedni": TipRacuna.STEDNI,
                "poslovni": TipRacuna.POSLOVNI,
            }
            if unos_tip not in mapa_tipova:
                raise ValueError(f"Nepoznat tip računa: {unos_tip}")
            tip = mapa_tipova[unos_tip]

            unos_val = input("Valuta (rsd/eur/usd): ").strip().lower()
            mapa_valuta = {"rsd": Valuta.RSD, "eur": Valuta.EUR, "usd": Valuta.USD}
            if unos_val not in mapa_valuta:
                raise ValueError(f"Nepoznata valuta: {unos_val}")
            val = mapa_valuta[unos_val]

            r = self.racun_svc.otvori_racun(v_id, tip, val)
            views.prikazi_uspeh(f"Uspešno otvoren račun sa ID: {r.id}")

        except ValueError as e:
            views.prikazi_gresku(f"Greška pri unosu: {e}")
        except Exception as e:
            views.prikazi_gresku(f"Neočekivana greška: {e}")

    def _zajednicka_promena_statusa(self) -> None:
        try:
            r_id = UUID(input("Unesite ID računa: ").strip())
            akcija = input("Izaberite (1: Blokiraj, 2: Odblokiraj, 3: Zatvori): ").strip()
            if akcija == "1":
                self.racun_svc.blokiraj_racun(r_id)
            elif akcija == "2":
                self.racun_svc.odblokiraj_racun(r_id)
            elif akcija == "3":
                self.racun_svc.zatvori_racun(r_id)
            views.prikazi_uspeh("Status računa je uspešno ažuriran.")
        except Exception as e:
            views.prikazi_gresku(f"Greška: {e}")

    def _radnik_registruj_klijenta(self) -> None:
        try:
            ime = input("Ime: ").strip()
            prezime = input("Prezime: ").strip()
            usr = input("Korisničko ime: ").strip()
            pwd = input("Lozinka: ").strip()
            novi = Klijent(ime=ime, prezime=prezime, username=usr, password=pwd)
            self.repo_korisnici.save(novi)
            views.prikazi_uspeh(f"Klijent registrovan! ID: {novi.id}")
        except Exception as e:
            views.prikazi_gresku(f"Greška: {e}")

    def _radnik_pregled_svih(self) -> None:
        for k in self.repo_korisnici.get_all():
            if k.uloga == Uloga.KLIJENT:
                print(f"\nKlijent: {k.ime} {k.prezime} [ID: {k.id}]")
                racuni = self.repo_racuni.get_by_vlasnik(k.id)
                for r in racuni:
                    print(f"  - Račun {r.id} | {r.tip.value} | {r.stanje:.2f} {r.valuta.value} [{r.status.value}]")

    # ==========================================
    # DIREKTOR MENI LOGIKA
    # ==========================================

    def _obradi_direktor_meni(self, izbor: str) -> None:
        if izbor == "0":
            self.trenutni_korisnik = None
            views.prikazi_uspeh("Odjavljeni ste.")
        elif izbor == "1":
            self._direktor_pregled_svih_racuna()
        elif izbor == "2":
            self._direktor_pregled_svih_transakcija()
        elif izbor == "3":
            self._zajednicka_promena_statusa()  # Blokiranje
        elif izbor == "4":
            self._direktor_pregled_klijenata()   # Usklađeno sa Opcijom 4 (Pregled liste svih klijenata)
        elif izbor == "5":
            self._zajednicka_promena_statusa()  # Usklađeno sa Opcijom 5 (Odblokiranje računa)
        elif izbor == "6":
            self._direktor_izvestaj_valute()
        else:
            views.prikazi_gresku("Nepoznata opcija.")

    def _direktor_pregled_svih_racuna(self) -> None:
        for r in self.repo_racuni.get_all():
            vlasnik = self.repo_korisnici.get_by_id(r.vlasnik_id)
            v_ime = f"{vlasnik.ime} {vlasnik.prezime}" if vlasnik else "Nepoznato"
            print(f"Račun: {r.id} | Vlasnik: {v_ime} | {r.tip.value} | Stanje: {r.stanje:.2f} {r.valuta.value} [{r.status.value}]")

    def _direktor_pregled_svih_transakcija(self) -> None:
        print("\n--- REGISTAR SVIH TRANSAKCIJA BANKE ---")
        for r in self.repo_racuni.get_all():
            for t in self.repo_transakcije.get_by_racun(r.id):
                print(f"  [{t.timestamp}] Račun: {r.id} | Tip: {t.tip} | Iznos: {t.iznos:.2f} {r.valuta.value}")

    def _direktor_pregled_klijenata(self) -> None:
        print("\n--- REGISTAR KLIJENATA BANKE ---")
        for k in self.repo_korisnici.get_all():
            if k.uloga == Uloga.KLIJENT:
                print(f"ID: {k.id} | Ime: {k.ime} {k.prezime} | Korisničko ime: {k.username}")

    def _direktor_izvestaj_valute(self) -> None:
        print("\n--- FINANSIJSKI IZVEŠTAJ SALDA PO VALUTAMA ---")
        izvestaj: dict[str, float] = {}
        for r in self.repo_racuni.get_all():
            izvestaj[r.valuta.value] = izvestaj.get(r.valuta.value, 0.0) + r.stanje
        for valuta, ukupno in izvestaj.items():
            print(f"  * {valuta}: {ukupno:,.2f}")