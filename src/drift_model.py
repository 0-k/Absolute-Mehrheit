import pandas as pd
import numpy as np

from data.data import data


class DriftModel:

    def __init__(self):
        self.date_from = pd.Timestamp('01-01-2020x')
        self.date_to = pd.Timestamp('15-11-2020')
        self.window = pd.Timedelta(20, 'W').round('d')
        self.date_range = pd.date_range(self.date_from, self.date_to)

    def calc_drift(self):
        drift = []
        for day in self.date_range:
            drift.append(np.std(data.loc[day:(day+self.window).date()]))
        drift = np.array(drift)
        drift = drift[~np.isnan(drift)]
        self.drift = drift

    def get_drift(self, party):
        return np.mean(self.drift.party)

