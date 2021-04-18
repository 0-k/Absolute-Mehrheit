import pandas as pd
import numpy as np

from parties import Party, UNION
from config.config import config
from dat.historic_poll_data import historic_poll_data


class DriftModel:

    def __init__(self, window: int = 200):
        self.values = historic_poll_data
        self.window = pd.Timedelta(window, 'days').round('d')
        self.__date_from = pd.Timestamp('2013-01-01')
        self.__date_to = pd.Timestamp('2020-11-15')
        self.__date_range = pd.date_range(self.__date_from, self.__date_to)

    def calc_drift(self, party: Party):
        data_by_party = self.values[party.name]
        drift = [np.std(data_by_party.loc[day:(day+self.window).date()]) for day in self.__date_range]
        drift = np.array(drift)
        drift = drift[~np.isnan(drift)]
        return np.mean(drift)/100


class PollModel:

    def __init__(self):
        self.values = historic_poll_data
        self.__date_from = None
        self.__date_to = None
        self.__date_range = None
        self.update_dates()

    def update_dates(self, date_to=pd.Timestamp('2020-11-01')):
        self.__date_to = date_to
        window = pd.Timedelta(50, 'days').round('d')
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
        decay_parameter = config['decay_parameter']
        decay = [(1/decay_parameter)**idx for idx in range(len(self.__date_range))]
        decay = pd.DataFrame(decay, index=self.__date_range[::-1], columns=['decay'])
        decay.index = pd.to_datetime(decay.index)
        return decay

    def __filter(self):
        data_filtered = self.values
        data_filtered.index  = pd.to_datetime(data_filtered.index)
        data_filtered = data_filtered.resample('d', axis=0).mean()
        try:
            data_filtered = data_filtered.loc[self.__date_from:self.__date_to]
        except KeyError:
            pass
        try:
            data_filtered = data_filtered.drop(['Institute', 'Total'], axis=1)
        except KeyError:
            pass
        return data_filtered.dropna()


if __name__ == '__main__':
    drift_model = DriftModel()
    poll_model = PollModel()
    print(drift_model.calc_drift(UNION))
    print(poll_model.calc_current_average())



