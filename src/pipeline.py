import pandas as pd
from datetime import date

from config.config import config
from dat.loader import Loader
from simulation import Simulation
import parties
import coalitions
import plotting
from src.models import DriftModel, PollModel


def load_polling_results():
    loader = Loader()
    polls_by_party = [loader.get_latest_percentages_of(party) for party in parties.ALL]
    dates = loader.get_latest_dates_of_polls()
    return __as_df(polls_by_party, dates)


def __as_df(polls_by_party, dates):
    df = pd.DataFrame.from_records(polls_by_party).T
    df.columns = [party.name for party in parties.ALL]
    df.index = dates
    return df.sort_index()


def aggregate(polls):
    poll_aggregation = PollModel()
    poll_aggregation.values = polls
    print()
    poll_aggregation.update_dates(pd.Timestamp(date.today()))
    return poll_aggregation.calc_current_average()


def determine_drift():
    drift = DriftModel()
    today = pd.Timestamp(date.today())
    election_day = pd.Timestamp(config['election_day'])
    drift.window = election_day - today
    return [drift.calc_drift(party) for party in parties.ALL]


def update_parties(polls, drift):
    for party in parties.ALL:
        party.percentage = polls[party.idx]
        party.uncertainty = polls[party.idx] * config['uncertainty']
        party.drift = drift[party.idx]


def simulate_elections():
    return Simulation(parties.ALL)


def evaluate_seats():
    names = [coalition.name for coalition in coalitions.ALL]
    seats_by_coalition = [simulation.evaluate_seats_by(coalition) for coalition in coalitions.ALL]
    return dict(zip(names, seats_by_coalition))


def calc_coalition_correlation(seats_by_coalition):
    df = pd.DataFrame(seats_by_coalition)
    return df.corr()


def evaluate_probability_hurdle_surpassing():
    return [simulation.evaluate_probability_hurdle_surpassing(party) for party in parties.CURRENT_PARLIAMENT]


def evaluate_if_majority(seats_by):
    majority = dict()
    for coalition in seats_by:
        majority[coalition] = [-1. if item < 300 else 1. for item in seats_by[coalition]]
    return majority


if __name__ == '__main__':
    polling_results = load_polling_results()
    polls = aggregate(polling_results)
    drift = determine_drift()
    update_parties(polls, drift)
    simulation = simulate_elections()
    seats_by_coalition = evaluate_seats()
    has_majority = evaluate_if_majority(seats_by_coalition)
    correlation = calc_coalition_correlation(seats_by_coalition)
    hurdles_surpassing_probability = evaluate_probability_hurdle_surpassing()

    print(has_majority)
    #plotting.plot_coalitions(seats_by_coalition)
    #plotting.plot_correlation(correlation)
    print(hurdles_surpassing_probability)

    #evaluate_coalition_without()
    #evaluate_coalition_with()
