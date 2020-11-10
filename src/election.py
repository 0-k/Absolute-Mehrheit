import pandas as pd
import numpy as np
from config.config import config


class Election:

    def __init__(self, result: np.array):
        self.result = result
        self.__drop_other_parties()
        self.number_of_parties = len(self.result)
        self.total_seats = config['TOTAL_SEATS']
        self.__enforce_five_percent_hurdle()

    def __drop_other_parties(self):
        self.result = self.result[:-1]

    def __enforce_five_percent_hurdle(self):
        threshold_idx = self.result < config['THRESHOLD_HURDLE']
        self.result[threshold_idx] = 0

    def calc_seats(self):
        # Sainte-Laguë procedure
        sainte_lague_quotients = self.__calc_sainte_lague_quotients()
        seats = self.__count_number_of_highest(sainte_lague_quotients)
        return seats

    def __calc_sainte_lague_quotients(self):
        sainte_lague_quotients = np.zeros((self.total_seats, self.number_of_parties))
        for idx in range(self.total_seats):
            sainte_lague_quotients[idx] = self.result / (idx + 0.5)
        return sainte_lague_quotients

    def __count_number_of_highest(self, quotients: np.array):
        seats = self.__filter_for_highest(quotients)
        return seats.count().values

    def __filter_for_highest(self, quotients):
        df = pd.DataFrame(quotients)
        lowest_accepted_value = np.sort(quotients.flatten())[::-1][self.total_seats - 1]
        df[df < lowest_accepted_value] = np.nan
        return df


