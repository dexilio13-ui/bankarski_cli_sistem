        >>>  Projektni zadatak : Bankarski CLI Sistem  <<<


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



