        >>>  Projektni zadatak : Bankarski CLI Sistem  <<<



### Sta je uradjeno do sada ###
-------------------------------

Faza 1 - Zavrseno sve osim: CLI sa Rich bibliotekom za formatirani ispis

Faza 2 - Zavrsena


--------------------------------

# Uputstvo za testiranje — Bankarski CLI Sistem

## Pokretanje

```powershell
cd E:\bankarski_cli_sistem
.venv\Scripts\activate
python main.py
```

---

## Kredencijali (seed podaci)

| Uloga | Username | Lozinka | Ime |
|---|---|---|---|
| Direktor | `admin` | `admin123` | Marko Kraljević |
| Radnik | `radnik1` | `pass1` | Jovan Jovanović |
| Radnik | `radnik2` | `pass2` | Ana Anić |
| Klijent | `pera` | `pera123` | Pera Perić |
| Klijent | `mika` | `mika123` | Mika Mikić |
| Klijent | `zika` | `zika123` | Žika Žikić |

---

## TEST 1 — Radnik: Registracija novog klijenta

**Prijava:**
```
>>> 1
Korisničko ime: radnik1
Lozinka: pass1
```

**Registracija (opcija 3):**
```
>>> 3
Ime klijenta: Nikola
Prezime klijenta: Nikolić
Korisničko ime: nikola
Lozinka: nikola123
```

**Očekivani rezultat:**
```
✅ USPEH: Klijent registrovan! ID: <uuid>
```
> ⚠️ Zapiši ispisani ID — treba ti u sledećem koraku!

---

## TEST 2 — Radnik: Otvaranje računa novom klijentu

Dok si još prijavljen kao `radnik1`, izaberi opciju 1:

```
>>> 1
ID klijenta: <ID iz testa 1>
Tip (tekuci/stedni/poslovni): tekuci
Valuta (rsd/eur/usd): rsd
```

**Očekivani rezultat:**
```
✅ USPEH: Uspešno otvoren račun: <uuid>
```

---

## TEST 3 — Radnik: Pregled klijenata i računa

```
>>> 5
```

**Očekivani rezultat:** Rich tabela sa svim klijentima (Pera, Mika, Žika, Nikola) i njihovim računima. Nikola treba da ima tekući RSD račun sa stanjem `0.00`.

---

## TEST 4 — Klijent: Uplata, isplata i transfer

**Prijava kao Nikola:**
```
>>> 1
Korisničko ime: nikola
Lozinka: nikola123
```

**Pregled računa (opcija 1):**
```
>>> 1
```
Vidiš tekući račun sa stanjem `0.00 rsd`. Zapiši ID računa.

**Uplata (opcija 2):**
```
>>> 2
ID računa: <ID iz pregleda>
Iznos uplate: 10000
```
**Očekivani rezultat:** `✅ USPEH: Uplata od 10000.00 uspešno izvršena.`

**Provera (opcija 1):** Stanje mora biti `10000.00 rsd`.

**Isplata (opcija 3):**
```
>>> 3
ID računa: <isti ID>
Iznos isplate: 3000
```
**Očekivani rezultat:** `✅ USPEH: Isplata od 3000.00 uspešno izvršena.`

**Provera (opcija 1):** Stanje mora biti `7000.00 rsd`.

**Pregled istorije (opcija 5):**
```
>>> 5
```
**Očekivani rezultat:** Tabela sa dve transakcije — uplata `+10000.00` i isplata `-3000.00`.

---

## TEST 5 — Klijent: Transfer između računa (Pera Perić)

Pera ima dva računa (tekući i štedni), idealan za test transfera.

**Prijava:**
```
>>> 1
Korisničko ime: pera
Lozinka: pera123
```

**Pregled računa (opcija 1):**
```
>>> 1
```
Zapiši ID tekućeg (RSD) i štednog (EUR) računa.

**Transfer (opcija 4):**
```
>>> 4
ID izvornog računa: <ID tekućeg>
ID ciljnog računa: <ID štednog>
Iznos transfera: 5000
```
**Očekivani rezultat:** `✅ USPEH: Transfer od 5000.00 uspešno izvršen.`

**Provera (opcija 1):** Tekući mora imati `45000.00 rsd`, štedni `10000.00 eur` (transfer ne konvertuje valutu).

---

## TEST 6 — Radnik: Blokiranje računa

**Prijava kao radnik1**, pa izaberi opciju 2:
```
>>> 2
ID računa za blokiranje: <ID Nikolinog računa>
```
**Očekivani rezultat:** `✅ USPEH: Račun je uspešno blokiran.`

**Provera — prijavi se kao Nikola i pokušaj isplatu (opcija 3):**
```
>>> 3
ID računa: <isti ID>
Iznos isplate: 100
```
**Očekivani rezultat:** `❌ GREŠKA: Nije dozvoljena isplata. Račun je trenutno BLOKIRAN.`

**Provera — uplata na blokiran račun (opcija 2):**
Uplata treba da prođe — blokiran račun prima uplate, ali ne dozvoljava isplate.

---

## TEST 7 — Radnik: Odblokiranje računa

**Prijava kao radnik1**, pa opcija 4:
```
>>> 4
ID računa za odblokiranje: <ID Nikolinog računa>
```
**Očekivani rezultat:** `✅ USPEH: Račun je uspešno odblokiran.`

**Provera — prijavi se kao Nikola i pokušaj isplatu ponovo.** Sad mora proći.

---

## TEST 8 — Direktor: Pregledi i izveštaji

**Prijava:**
```
>>> 1
Korisničko ime: admin
Lozinka: admin123
```

**Pregled svih računa (opcija 1):**
Tabela sa svim računima svih klijenata, vlasnicima, stanjima i statusima.

**Pregled svih transakcija (opcija 2):**
Sve transakcije iz sistema — uplate zeleno `+`, isplate crveno `-`.

**Pregled klijenata (opcija 4):**
Lista svih klijenata sa ID-evima — mora biti vidljiv i Nikola (registrovan u testu 1).

**Izveštaj po valutama (opcija 6):**
Zbir svih stanja grupisanih po valuti. Nakon testova mora biti drugačije od početnih vrednosti:
- RSD: promenjen (uplate/isplate/transferi)
- EUR: `10000.00` (štedni Perin, nije menjan)

**Blokiranje (opcija 3) i odblokiranje (opcija 5):**
Isto kao radnikove opcije 2 i 4 — unosi se ID računa.

---

## TEST 9 — Negativni scenariji (greške)

| Akcija | Očekivana greška |
|---|---|
| Pogrešna lozinka pri prijavi | `❌ GREŠKA: Neispravno korisničko ime ili lozinka.` |
| Isplata veća od stanja (bez dozvoljenog minusa) | `❌ GREŠKA: Nedovoljno sredstava na računu.` |
| Isplata sa blokiranog računa | `❌ GREŠKA: Nije dozvoljena isplata. Račun je trenutno BLOKIRAN.` |
| Registracija sa već zauzetim username-om | `❌ GREŠKA: Korisničko ime '...' je već zauzeto.` |
| Unos tuđeg ID računa pri uplati/isplati | `❌ GREŠKA: Račun ne pripada vašem nalogu.` |
| Transfer ako klijent ima samo 1 račun | `Potrebna su najmanje dva računa za transfer.` |

---

## Napomene

- Podaci se čuvaju u `banka.db` — sve izmene ostaju i posle restarta.
- Za reset na početno stanje: obrišite `banka.db` i ponovo pokrenite `python main.py`.


