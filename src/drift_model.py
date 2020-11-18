import pandas as pd
import numpy as np

from data.data import data


class DriftModel:

    def __init__(self):
        self.date_from = pd.Timestamp('01-01-2013')
        self.date_to = pd.Timestamp('15-11-2020')
        self.window = pd.Timedelta(40, 'W').round('d')
        self.date_range = pd.date_range(self.date_from, self.date_to)

    def calc_drift(self, party):
        data_by_party = data[party]
        drift = []
        for day in self.date_range:
            drift_by_day = np.std(data_by_party.loc[day:(day+self.window).date()])
            drift.append(drift_by_day)
        drift = np.array(drift)
        drift = drift[~np.isnan(drift)]
        return np.mean(drift)


if __name__ == '__main__':
    model = DriftModel()
    print(model.calc_drift('Union'))

