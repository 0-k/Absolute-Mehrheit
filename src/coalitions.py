from itertools import count
from dataclasses import dataclass, field

import parties

counter = count()


@dataclass
class Coalition:
    name: str
    parties: [parties.Party]
    idx: int = field(default_factory=lambda: next(counter))

    def __contains__(self, party: parties.Party):
        if party in self.parties:
            return True
        else:
            return False


BLACK_GREEN = Coalition('BLACK_GREEN', [parties.UNION, parties.GRUENE])
BLACK_RED = Coalition('BLACK_RED', [parties.UNION, parties.SPD])
GREEN_RED_RED = Coalition('GREEN_RED_RED', [parties.GRUENE, parties.SPD, parties.LINKE])
GREEN_RED_YELLOW = Coalition('GREEN_RED_YELLOW', [parties.GRUENE, parties.SPD, parties.FDP])
BLACK_YELLOW = Coalition('BLACK_YELLOW', [parties.UNION, parties.FDP])
BLACK_GREEN_YELLOW = Coalition('BLACK_GREEN_YELLOW', [parties.UNION, parties.GRUENE, parties.FDP])
ALL = [BLACK_GREEN, BLACK_RED, BLACK_GREEN_YELLOW, BLACK_YELLOW, GREEN_RED_RED, GREEN_RED_YELLOW]

if __name__ == '__main__':
    for coalition in ALL:
        print()
        print(coalition.name)
        for party in parties.ALL:
            print(party.name)
            print(party in coalition)
