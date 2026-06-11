"""
core/exceptions.py — Prilagođeni izuzeci za domen banke.
💭 Hijerarhija omogućava da u CLI-ju uhvatimo "BankaError"
    i korisniku prikažemo lepu poruku umesto pucanja programa.
"""

class BankaError(Exception):
    """Osnovna klasa za sve specifične bankarske greške."""
    pass

class NedovoljnoSredstavaError(BankaError):
    """Baca se kada račun nema dovoljno sredstava (ili prelazi dozvoljeni minus)."""
    pass

class StatusRacunaError(BankaError):
    """Baca se kada se pokuša nedozvoljena operacija nad blokiranim/zatvorenim računom."""
    pass

class AutentifikacijaError(BankaError):
    """Baca se kada korisnik unese pogrešno korisničko ime ili lozinku."""
    pass