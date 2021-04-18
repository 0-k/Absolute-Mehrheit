import numpy as np
import math

from election import Election
from parties import Party
from coalitions import Coalition
from config.config import config


class Simulation:

    def __init__(self, parties: [Party], drop_other_parties: bool = False):
        self.values = None
        self.__parties = parties
        self.__sample_size = config['sample_size']
        self.__number_of_parties = len(self.__parties)
        self.__drop_other_parties = drop_other_parties
        self.__initialize_samples()

    def __initialize_samples(self):
        samples = np.zeros((self.__number_of_parties, self.__sample_size))
        for idx in range(self.__number_of_parties):
            party = self.__parties[idx]
            total_error = math.sqrt(party.uncertainty**2 + party.drift**2)
            samples[idx] = np.random.normal(party.percentage, total_error, self.__sample_size)
        samples[samples < 0] = 0
        total_result = samples.sum(axis=0)
        samples /= total_result
        self.values = samples

    def evaluate_seats_by(self, coalition: Coalition):
        coalition_seats = np.zeros(self.__sample_size)
        for idx in range(self.__sample_size):
            election_result = self.values.T[idx]
            election = Election(election_result, drop_other_parties=self.__drop_other_parties)
            seats_by_party = election.calc_seats_by_party()
            for party in coalition.parties:
                coalition_seats[idx] += seats_by_party[party.idx]
        return coalition_seats

    def evaluate_probability_hurdle_surpassing(self, party):
        seats = np.zeros(self.__sample_size)
        for idx in range(self.__sample_size):
            election_result = self.values.T[idx]
            election = Election(election_result, drop_other_parties=self.__drop_other_parties)
            seats_by_party = election.calc_seats_by_party()
            seats[idx] = seats_by_party[party.idx]
        return np.count_nonzero(seats)/self.__sample_size

    def __repr__(self):
        return str(self.values)
