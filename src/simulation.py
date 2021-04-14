import numpy as np
import math

from election import Election
from parties import Party
from coalitions import Coalition
from config.config import config


class Simulation:

    def __init__(self, parties: [Party]):
        self.parties = parties
        self.sample_size = config['sample_size']
        self.number_of_parties = len(self.parties)
        self.samples = None
        self.drop_other_parties = True
        self.__initialize_samples()

    def __initialize_samples(self):
        samples = np.zeros((self.number_of_parties, self.sample_size))
        for idx in range(self.number_of_parties):
            party = self.parties[idx]
            total_error = math.sqrt(party.uncertainty**2 + party.drift**2)
            samples[idx] = np.random.normal(party.percentage, total_error, self.sample_size)
        samples[samples < 0] = 0
        total_result = samples.sum(axis=0)
        samples /= total_result
        self.samples = samples

    def evaluate_seats_by(self, coalition: Coalition):
        coalition_seats = np.zeros(self.sample_size)
        for idx in range(self.sample_size):
            election_result = self.samples.T[idx]
            election = Election(election_result, drop_other_parties=self.drop_other_parties)
            seats_by_party = election.calc_seats_by_party()
            for party in coalition.parties:
                coalition_seats[idx] += seats_by_party[party.idx]
        return coalition_seats

    def evaluate_probability_hurdle_surpassing(self, party):
        seats = np.zeros(self.sample_size)
        for idx in range(self.sample_size):
            election_result = self.samples.T[idx]
            election = Election(election_result, drop_other_parties=self.drop_other_parties)
            seats_by_party = election.calc_seats_by_party()
            seats[idx] = seats_by_party[party.idx]
        return np.count_nonzero(seats)/self.sample_size
