"""
core/decorators.py — Dekoratori za poslovnu logiku.

💭 Zašto ovaj modul: Implementira Decorator pattern za proširenje funkcionalnosti
    bez menjanja originalnog koda.
"""

from functools import wraps


def isplatiti_sa_provizijom(provizija: float):
    """
    Dekorator koji dodaje proviziju na svaku isplatu.
    Args:
        provizija (float): Iznos provizije (npr. 50 dinara).
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Pretpostavljamo da originalna funkcija prima `iznos` kao argument
            iznos = kwargs.get("iznos") or (args[1] if len(args) > 1 else None)
            if iznos is None:
                raise ValueError("Dekorator očekuje argument 'iznos'.")

            # Dodajemo proviziju na iznos
            ukupno = iznos + provizija
            print(f"[DECORATOR] Isplata {iznos} + provizija {provizija} = {ukupno}")

            # Pozivamo originalnu funkciju sa novim iznosom
            if "iznos" in kwargs:
                kwargs["iznos"] = ukupno
            else:
                args = (args[0], ukupno, *args[2:])

            return func(*args, **kwargs)

        return wrapper

    return decorator


# ENTRY POINT TEST -

if __name__ == "__main__":
    # Primer funkcije koja simulira isplatu
    @isplatiti_sa_provizijom(provizija=50)
    def isplata(racun_id, iznos):
        print(f"Isplaćeno {iznos} sa računa {racun_id}")

    # Test
    isplata("123-456", 500)
