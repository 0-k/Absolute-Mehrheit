from itertools import count
from dataclasses import dataclass, field

import party

counter = count()


@dataclass
class Coalition:
    name: str
    parties: [party.Party]
    idx: int = field(default_factory=lambda: next(counter))


BLACK_GREEN = Coalition('BLACK_GREEN', [party.UNION, party.GRUENE])
BLACK_RED = Coalition('BLACK_RED', [party.UNION, party.SPD])
GREEN_RED_RED = Coalition('GREEN_RED_RED', [party.GRUENE, party.SPD, party.LINKE])
GREEN_RED_YELLOW = Coalition('GREEN_RED_YELLOW', [party.GRUENE, party.SPD, party.FDP])
BLACK_YELLOW = Coalition('BLACK_YELLOW', [party.UNION, party.FDP])
BLACK_GREEN_YELLOW = Coalition('BLACK_GREEN_YELLOW', [party.UNION, party.GRUENE, party.FDP])
