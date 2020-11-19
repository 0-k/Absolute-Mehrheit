import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from data.data import data
#print(data)

class DriftModel:

    def __init__(self):
        self.date_from = pd.Timestamp('2013-01-01')
        self.date_to = pd.Timestamp('2020-11-15')
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


class PollModel:

    def __init__(self):
        self.date_to = pd.Timestamp('2020-11-03')
        self.window = pd.Timedelta(8, 'W').round('d')
        self.date_from = (self.date_to - self.window).date()
        self.date_range = pd.date_range(self.date_from, self.date_to)

    def filter_data(self):
        data_filtered = data.loc[self.date_from:self.date_to]
        return data_filtered

    def calc_decay(self):
        decay = []
        decay_parameter = 1 + 0.105
        for idx in range(len(self.date_range)):
            decay.append((1/decay_parameter)**idx)
        decay = pd.DataFrame(decay, index=self.date_range[::-1], columns=['decay'])
        return decay

    def join(self):
        decay = self.calc_decay()
        data_filtered = self.filter_data()
        result = pd.concat([data_filtered, decay], axis=1, join='inner')
        print(sum(result.decay))
        #divide all data_filtered by sum
        #multiply all rows by decay value
        #take sum of all columns


if __name__ == '__main__':
    drift_model = DriftModel()
    poll_model = PollModel()
    #poll_model.filter_data()
    poll_model.join()

    #print(model.calc_drift('Union'))


