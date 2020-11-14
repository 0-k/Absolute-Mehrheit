from itertools import count


class Party:
    _idxs = count(0)

    def __init__(self, name: str, percentage: float, uncertainty: float, drift: float = 0., idx: int = 0):
        self.name = name
        self.percentage = percentage
        self.uncertainty = uncertainty
        self.drift = drift
        self.idx = next(self._idxs)
