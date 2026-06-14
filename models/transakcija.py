"""
models/transakcija.py — Model za beleženje promena stanja.

💭 Zašto ovaj modul: Beleženje promena stanja u arhitekturi.
🔁 Odabir:  Clean Rewrite - jedan definisani model.

"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Transakcija:
    """Predstavlja istorijski zapis o izvršenoj transakciji.

    💭 Zašto ova klasa: Služi isključivo kao DTO/Zapis (domen logike).
    🔁 Odabir: Korišćenje float tipa osigurava usklađenost sa Racun.stanje.

    Attributes:
        racun_id (UUID): UUID računa na kojem je izvršena promjena.
        iznos (float): Iznos uplate/isplate.
        tip (str): Opis transakcije (npr. 'UPLATA', 'ISPLATA').
        id (UUID): Auto-generisani ID.
        timestamp (datetime): Auto-generisano vrijeme kreiranja.
    """

    racun_id: UUID
    iznos: float
    tip: str
    id: UUID = field(default_factory=uuid4)

    #  init=False sprečava da mypy baca grešku kad se instancira klasa,
    # a dataclass će sam pozvati datetime.now() prilikom kreiranja instance.
    timestamp: datetime = field(default_factory=datetime.now, init=False)
