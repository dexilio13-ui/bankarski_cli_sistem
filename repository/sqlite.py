"""
repository/sqlite.py — SQLite implementacija repozitorijuma (Faza 2).
💭 Enkapsulira SQL upite i omogućava perzistenciju podataka.
"""

import sqlite3
from pathlib import Path
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime

from models.korisnik import Korisnik
from models.racun import Racun
from models.transakcija import Transakcija
from models.enums import Uloga, TipRacuna, Valuta, StatusRacuna
from repository.interfaces import KorisnikRepo, RacunRepo, TransakcijaRepo

DB_PATH = Path("banka.db")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS korisnici (
    id TEXT PRIMARY KEY,
    ime TEXT NOT NULL,
    prezime TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    uloga TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS racuni (
    id TEXT PRIMARY KEY,
    vlasnik_id TEXT NOT NULL,
    tip TEXT NOT NULL,
    valuta TEXT NOT NULL,
    stanje REAL NOT NULL,
    status TEXT NOT NULL,
    kamatna_stopa REAL,
    dozvoljeni_minus REAL
);
CREATE TABLE IF NOT EXISTS transakcije (
    id TEXT PRIMARY KEY,
    racun_id TEXT NOT NULL,
    iznos REAL NOT NULL,
    tip TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
"""

def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA_SQL)


class SQLiteKorisnikRepo(KorisnikRepo):
    def get_by_id(self, korisnik_id: UUID) -> Korisnik | None:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("SELECT * FROM korisnici WHERE id=?", (str(korisnik_id),))
            row = cur.fetchone()
            return self._mapiraj_u_objekat(row) if row else None

    def get_by_username(self, username: str) -> Korisnik | None:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("SELECT * FROM korisnici WHERE username=?", (username,))
            row = cur.fetchone()
            return self._mapiraj_u_objekat(row) if row else None

    def get_all(self) -> List[Korisnik]:
        """Vraća listu svih korisnika iz baze."""
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("SELECT * FROM korisnici")
            return [self._mapiraj_u_objekat(row) for row in cur.fetchall()]

    def save(self, k: Korisnik) -> None:
         with sqlite3.connect(DB_PATH) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO korisnici (id, ime, prezime, username, password, uloga)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (str(k.id), k.ime, k.prezime, k.username, k.password, k.uloga.value))

    def _mapiraj_u_objekat(self, row: tuple) -> Korisnik:
        return Korisnik(
            id=UUID(row[0]), ime=row[1], prezime=row[2],
            username=row[3], password=row[4], uloga=Uloga(row[5])
        )


class SQLiteRacunRepo(RacunRepo):
    def get_by_id(self, racun_id: UUID) -> Racun | None:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("SELECT * FROM racuni WHERE id=?", (str(racun_id),))
            row = cur.fetchone()
            return self._mapiraj_u_objekat(row) if row else None

    def get_by_vlasnik(self, vlasnik_id: UUID) -> List[Racun]:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("SELECT * FROM racuni WHERE vlasnik_id=?", (str(vlasnik_id),))
            return [self._mapiraj_u_objekat(row) for row in cur.fetchall()]

    def get_all(self) -> List[Racun]:
        """Vraća listu svih računa iz baze."""
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("SELECT * FROM racuni")
            return [self._mapiraj_u_objekat(row) for row in cur.fetchall()]

    def save(self, r: Racun) -> None:
         with sqlite3.connect(DB_PATH) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO racuni 
                (id, vlasnik_id, tip, valuta, stanje, status, kamatna_stopa, dozvoljeni_minus)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                 str(r.id), str(r.vlasnik_id), r.tip.value, r.valuta.value,
                 r.stanje, r.status.value, r.kamatna_stopa, r.dozvoljeni_minus
            ))

    def _mapiraj_u_objekat(self, row: tuple) -> Racun:
        return Racun(
            id=UUID(row[0]), vlasnik_id=UUID(row[1]), tip=TipRacuna(row[2]),
            valuta=Valuta(row[3]), stanje=row[4], status=StatusRacuna(row[5]),
            kamatna_stopa=row[6], dozvoljeni_minus=row[7]
        )


class SQLiteTransakcijaRepo(TransakcijaRepo):
    def get_by_racun(self, racun_id: UUID) -> List[Transakcija]:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("SELECT * FROM transakcije WHERE racun_id=?", (str(racun_id),))
            return [self._mapiraj_u_objekat(row) for row in cur.fetchall()]

    def save(self, t: Transakcija) -> None:
        with sqlite3.connect(DB_PATH) as conn:
             conn.execute('''
                INSERT OR REPLACE INTO transakcije (id, racun_id, iznos, tip, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (str(t.id), str(t.racun_id), t.iznos, t.tip, t.timestamp.isoformat()))

    def _mapiraj_u_objekat(self, row: tuple) -> Transakcija:
        t = Transakcija(id=UUID(row[0]), racun_id=UUID(row[1]), iznos=row[2], tip=row[3])
        t.timestamp = datetime.fromisoformat(row[4])
        return t


def seed_data() -> None:
    """Popunjava bazu početnim podacima tačno prema tehničkoj specifikaciji."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM korisnici")
        if cursor.fetchone()[0] == 0:
            print("🌱 Baza je prazna, dodajem početne podatke po specifikaciji...")

            # 1. Generisanje fiksnih ID-jeva kako bismo ispravno povezali račune sa vlasnicima
            id_marko = str(uuid4())
            id_jovan = str(uuid4())
            id_ana = str(uuid4())
            id_pera = str(uuid4())
            id_mika = str(uuid4())
            id_zika = str(uuid4())

            # 2. Ubacivanje početnih naloga (Korisnici)
            korisnici = [
                (id_marko, "Marko", "Kraljević", "admin", "admin123", Uloga.DIREKTOR.value),
                (id_jovan, "Jovan", "Jovanović", "radnik1", "pass1", Uloga.RADNIK.value),
                (id_ana, "Ana", "Anić", "radnik2", "pass2", Uloga.RADNIK.value),
                (id_pera, "Pera", "Perić", "pera", "pera123", Uloga.KLIJENT.value),
                (id_mika, "Mika", "Mikić", "mika", "mika123", Uloga.KLIJENT.value),
                (id_zika, "Žika", "Žikić", "zika", "zika123", Uloga.KLIJENT.value)
            ]

            conn.executemany(
                "INSERT INTO korisnici (id, ime, prezime, username, password, uloga) VALUES (?, ?, ?, ?, ?, ?)",
                korisnici
            )

            # 3. Ubacivanje početnih računa vezanih za kreirane klijente
            # Formati kolona: id, vlasnik_id, tip, valuta, stanje, status, kamatna_stopa, dozvoljeni_minus
            racuni = [
                # Pera Perić nalozi
                (str(uuid4()), id_pera, TipRacuna.TEKUCI.value, Valuta.RSD.value, 50000.0, StatusRacuna.AKTIVAN.value, None, None),
                (str(uuid4()), id_pera, TipRacuna.STEDNI.value, Valuta.EUR.value, 10000.0, StatusRacuna.AKTIVAN.value, 0.03, None),
                # Mika Mikić nalozi
                (str(uuid4()), id_mika, TipRacuna.TEKUCI.value, Valuta.RSD.value, 25000.0, StatusRacuna.AKTIVAN.value, None, None),
                (str(uuid4()), id_mika, TipRacuna.POSLOVNI.value, Valuta.RSD.value, 100000.0, StatusRacuna.AKTIVAN.value, None, 50000.0),
                # Žika Žikić nalozi
                (str(uuid4()), id_zika, TipRacuna.TEKUCI.value, Valuta.RSD.value, 15000.0, StatusRacuna.AKTIVAN.value, None, None)
            ]

            conn.executemany(
                "INSERT INTO racuni (id, vlasnik_id, tip, valuta, stanje, status, kamatna_stopa, dozvoljeni_minus) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                racuni
            )

            print("✅ Početni nalozi i računi uspešno uvezeni u SQLite bazu podataka.")