from itertools import count
from dataclasses import dataclass, field

counter = count()


@dataclass
class Party:
    name: str
    id: str
    percentage: float = 0.0
    uncertainty: float = 0.0
    drift: float = 0.0
    idx: int = field(default_factory=lambda: next(counter))
