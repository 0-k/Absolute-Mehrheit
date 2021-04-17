import pandas as pd
import numpy as np

from dat.historic_poll_data import historic_poll_data


class DriftModel:

    def __init__(self):
        self.date_from = pd.Timestamp('2013-01-01')
        self.date_to = pd.Timestamp('2020-11-15')
        self.window = pd.Timedelta(40, 'W').round('d')
        self.date_range = pd.date_range(self.date_from, self.date_to)
        self.data = historic_poll_data

    def calc_drift(self, party):
        data_by_party = self.data[party]
        drift = []
        for day in self.date_range:
            drift_by_day = np.std(data_by_party.loc[day:(day+self.window).date()])
            drift.append(drift_by_day)
        drift = np.array(drift)
        drift = drift[~np.isnan(drift)]
        return np.mean(drift)


class PollModel:

    def __init__(self):
        self.__date_to = None
        self.__date_from = None
        self.__date_range = None
        self.update_dates()
        self.data = historic_poll_data

    def update_dates(self, date_to=pd.Timestamp('2021-04-17')):
        self.__date_to = date_to
        window = pd.Timedelta(8, 'W').round('d')
        self.__date_from = (self.__date_to - window).date()
        self.__date_range = pd.date_range(self.__date_from, self.__date_to)

    def calc_current_average(self):
        decay = self.__calc_decay()
        data_filtered = self.__filter()
        decay = pd.concat([data_filtered, decay], axis=1, join='inner').decay
        data_scaled = data_filtered/sum(decay)
        data_convoluted = data_scaled.mul(decay, axis=0)
        return np.sum(data_convoluted)/100

    def __calc_decay(self):
        decay = []
        decay_parameter = 1 + 0.3
        for idx in range(len(self.__date_range)):
            decay.append((1/decay_parameter)**idx)
        decay = pd.DataFrame(decay, index=self.__date_range[::-1], columns=['decay'])
        return decay

    def __filter(self):
        data_filtered = self.data
        try:
            data_filtered = self.data.loc[self.__date_from:self.__date_to]
        except KeyError:
            pass
        try:
            data_filtered = data_filtered.drop(['Institute', 'Total'], axis=1)
        except KeyError:
            pass
        return data_filtered


if __name__ == '__main__':
    drift_model = DriftModel()
    poll_model = PollModel()
    print(drift_model.calc_drift('UNION'))
    print(poll_model.calc_current_average())



