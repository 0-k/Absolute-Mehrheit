class Party:

    def __init__(self, name: str, percentage: float, uncertainty: float, drift: float = 0.):
        self.name = name
        self.percentage = percentage
        self.uncertainty = uncertainty
        self.drift = drift

