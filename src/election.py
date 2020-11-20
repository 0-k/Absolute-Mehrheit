import numpy as np
from config.config import config


class Election:

    def __init__(self, result: np.array, drop_other_parties: bool = False):
        self.result = result
        if drop_other_parties:
            self.__drop_other_parties()
        self.number_of_parties = len(self.result)
        self.total_seats = config['total_seats']
        self.__enforce_five_percent_hurdle()

    def __drop_other_parties(self):
        self.result = self.result[:-1]

    def __enforce_five_percent_hurdle(self):
        threshold_hurdle = self.result < config['threshold_hurdle']
        self.result[threshold_hurdle] = 0

    def calc_seats_by_party(self):
        # Sainte-Laguë procedure
        sainte_lague_quotients = self.__calc_sainte_lague_quotients()
        seats = self.__count_number_of_highest(sainte_lague_quotients)
        return seats

    def __calc_sainte_lague_quotients(self):
        divisors = np.arange(0.5, self.total_seats)
        sainte_lague_quotients = self.result / np.vstack(divisors)
        return sainte_lague_quotients

    def __count_number_of_highest(self, quotients: np.array):
        highest_sainte_lague_quotients = self.__filter_for_highest(quotients)
        seats = np.count_nonzero(highest_sainte_lague_quotients, axis=0)
        return seats

    def __filter_for_highest(self, quotients):
        lowest_accepted_value = np.sort(quotients.flatten())[::-1][self.total_seats - 1]
        quotients[quotients < lowest_accepted_value] = 0
        return quotients


