from itertools import count
from dataclasses import dataclass, field

counter = count()


@dataclass
class Party:
    name: str
    id: str
    percentage: float = 0.1
    uncertainty: float = 0.01
    drift: float = 0.01
    idx: int = field(default_factory=lambda: next(counter))

    def determine_errors(self):
        pass


UNION = Party(name='UNION', id='cdu')
SPD = Party(name='SPD', id='spd')
GRUENE = Party(name='GRUENE', id='gru')
FDP = Party(name='FDP', id='fdp')
LINKE = Party(name='LINKE', id='lin')
AFD = Party(name='AFD', id='afd')
OTHER = Party(name='OTHER', id='son')
ALL = [UNION, SPD, GRUENE, FDP, LINKE, AFD, OTHER]
CURRENT_PARLIAMENT = [UNION, SPD, GRUENE, FDP, LINKE, AFD]
