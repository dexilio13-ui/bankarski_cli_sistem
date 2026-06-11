        >>>  Projektni zadatak : Bankarski CLI Sistem  <<<

STRUKTURA DIREKTORIJUMA i FAJLOVA:
--------------------------------

bankarski_cli_sistem/
├── pyproject.toml           # Konfiguracija projekta i upravljanje zavisnostima (uv)
├── main.py                  # Ulazna tačka aplikacije (Entry point)
├── core/                    # Esencijalni mehanizmi sistema
│   ├── __init__.py
│   ├── exceptions.py        # Custom error handling (npr. NedovoljnoSredstavaError, RacunBlokiranError)
│   ├── events.py            # EventBus implementacija (Observer pattern)
│   └── decorators.py        # Dekoratori (npr. isplatiti_sa_provizijom)
├── models/                  # Domen aplikacije (Samo struktura podataka i osnovna logika)
│   ├── __init__.py
│   ├── enums.py             # TipRacuna, Valuta, Uloga, StatusRacuna  
│   ├── korisnik.py          # Klase: Korisnik, Direktor, Radnik, Klijent
│   ├── racun.py             # Klase računa i tranziciona mapa (State pattern)
│   └── transakcija.py       # Model za beleženje promena stanja
├── repository/              # Sloj za perzistenciju podataka (Repository pattern)
│   ├── __init__.py
│   ├── interfaces.py        # Apstraktne klase (@abstractmethod) za KorisnikRepo, RacunRepo
│   ├── memory.py            # In-memory dict/list implementacija (Faza 1)
│   └── sqlite.py            # SQLite implementacija (Faza 2)
├── services/                # Biznis logika sistema (Services)
│   ├── __init__.py
│   ├── banka.py             # Centralna Banka klasa (Singleton)
│   ├── racun_service.py     # Logika otvaranja (Factory),
│   ├── kamata_service.py    # Obračun kamate (Strategy pattern)
│   └── auth_service.py      # Autentifikacija, seed korisnici i role
└── cli/                     # Prezentacioni sloj (Isključivo prikaz i unos)
    ├── __init__.py
    ├── app.py               # Inicijalizacija CLI aplikacije
    ├── menus.py             # Logika menija za direktora, radnika, klijenta
    └── views.py             # Formatiranje tabele i panela pomoću 'rich' biblioteke
---------------------------------------------------------------------------------------


### Sta je uradjeno do sada ###
-------------------------------

Faza 1 - Zavrseno sve osim: CLI sa Rich bibliotekom za formatirani ispis

Faza 2 - Zavrsena


--------------------------------


PRIMER KORISCENJA:
-----------------

1 Korak: Radnik (Registracija i Otvaranje računa)

Prvo ćemo napraviti klijenta da imamo šta da testiramo.

Prijava: Izaberi 1.

Username: radnik

Lozinka: radnik123

Registracija klijenta (Opcija 3):

Unesi ime: Pera, prezime: Perić, username: pera, lozinka: pera123.

VAŽNO: Sistem će ispisati ID klijenta. Zapiši ga negde (ili kopiraj), trebaće ti odmah!


Otvaranje računa (Opcija 1):

Unesi ID klijenta koji si malopre zapisao.

Tip računa: TEKUCI

Valuta: RSD

Odjava: Izaberi 0.
-----------------------------------

2. Korak: Klijent (Transakcije)
Sada ćemo proveriti da li tvoj sistem ispravno beleži uplate.

Prijava: Izaberi 1.

Username: pera

Lozinka: pera123

Pregled stanja (Opcija 1):

Trebalo bi da vidiš svoj novi račun sa stanjem 0.00.

Uplata (Opcija 2):

Unesi ID računa (vidiš ga u pregledu stanja).

Iznos: 5000

Provera: Opet izaberi opciju 1. Stanje sada mora biti 5000.00.

Odjava: Izaberi 0.
------------------------------


3. Korak: Direktor (Izveštaji)
Ovo je trenutak istine za našu get_all popravku.

Prijava: Izaberi 1.

Username: direktor

Lozinka: admin123

Pregled klijenata (Opcija 4):

Ako vidiš Peru Perića na spisku, SQLiteKorisnikRepo.get_all() radi savršeno.

Pregled svih računa (Opcija 1):

Ako vidiš Perin račun i njegovo stanje, SQLiteRacunRepo.get_all() radi savršeno.

Izveštaj po valutama (Opcija 6):

Trebalo bi da vidiš RSD: 5000.00



