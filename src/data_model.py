import pandas as pd
import numpy as np
from data.data import historic_poll_data


class DriftModel:

    def __init__(self):
        self.date_from = pd.Timestamp('2013-01-01')
        self.date_to = pd.Timestamp('2020-11-15')
        self.window = pd.Timedelta(40, 'W').round('d')
        self.date_range = pd.date_range(self.date_from, self.date_to)

    def calc_drift(self, party):
        data_by_party = historic_poll_data[party]
        drift = []
        for day in self.date_range:
            drift_by_day = np.std(data_by_party.loc[day:(day+self.window).date()])
            drift.append(drift_by_day)
        drift = np.array(drift)
        drift = drift[~np.isnan(drift)]
        return np.mean(drift)


class PollModel:

    def __init__(self):
        self.date_to = pd.Timestamp('2020-11-18')
        self.window = pd.Timedelta(8, 'W').round('d')
        self.date_from = (self.date_to - self.window).date()
        self.date_range = pd.date_range(self.date_from, self.date_to)

    def calc_current_average(self):
        decay = self.__calc_decay()
        data_filtered = historic_poll_data.loc[self.date_from:self.date_to].drop(['Institute', 'Total'], axis=1)
        decay = pd.concat([data_filtered, decay], axis=1, join='inner').decay
        data_scaled = data_filtered/sum(decay)
        data_convoluted = data_scaled.mul(decay, axis=0)
        return np.sum(data_convoluted)/100

    def __calc_decay(self):
        decay = []
        decay_parameter = 1 + 0.105
        for idx in range(len(self.date_range)):
            decay.append((1/decay_parameter)**idx)
        decay = pd.DataFrame(decay, index=self.date_range[::-1], columns=['decay'])
        return decay


if __name__ == '__main__':
    drift_model = DriftModel()
    poll_model = PollModel()
    print(drift_model.calc_drift('Union'))
    print(poll_model.calc_current_average())



