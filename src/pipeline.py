import pandas as pd
import numpy as np
from datetime import date

from config.config import config
from dat.loader import Loader
from simulation import Simulation
from models import DriftModel, PollModel
import parties
import coalitions
import plotting


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


def calc_seats_by_coalition():
    names = [coalition.name for coalition in coalitions.ALL]
    seats = [simulation.calc_seats_by(coalition) for coalition in coalitions.ALL]
    return dict(zip(names, seats))


def calc_coalition_correlation(seats_by_coalition):
    df = pd.DataFrame(seats_by_coalition)
    return df.corr()


def calc_probability_hurdle_surpassing() -> dict:
    party_names = [party.name for party in parties.CURRENT_PARLIAMENT]
    probability = [simulation.calc_probability_hurdle_surpassing(party) for party in parties.CURRENT_PARLIAMENT]
    return dict(zip(party_names, probability))


def calc_has_majority_by_coalition() -> pd.DataFrame:
    majority = dict()
    for coalition in seats_by_coalition:
        majority[coalition] = [0 if item < config['majority'] else 1 for item in seats_by_coalition[coalition]]
    return pd.DataFrame(majority)


def calc_share_of_majority_by_coalition() -> dict:
    return dict(has_majority_by_coalition.sum()/config['sample_size'])


def calc_share_with_any_majority_by_party() -> dict:
    with_any_majority = dict()
    for party in parties.ALL:
        coalition_with_party = [coalition.name if (party in coalition) else None for coalition in coalitions.ALL]
        while None in coalition_with_party:
            coalition_with_party.remove(None)
        party_with_any_majority = has_majority_by_coalition[coalition_with_party]
        with_any_majority[party.name] = party_with_any_majority.any(axis=1).sum() / config['sample_size']
    return with_any_majority


def calc_share_with_no_majority() -> float:
    with_no_majority = 1 - has_majority_by_coalition.any(axis=1).sum() / config['sample_size']
    return float(with_no_majority)


def calc_dependent_majority(while_majority_of_coalition: coalitions.Coalition,
                            dependent_coalition: coalitions.Coalition) -> float:
    dependent_majority = has_majority_by_coalition[has_majority_by_coalition[while_majority_of_coalition.name] == 1]
    if dependent_majority[while_majority_of_coalition.name].sum() == 0:
        return np.nan
    return dependent_majority[dependent_coalition.name].sum()/dependent_majority[while_majority_of_coalition.name].sum()


def calc_dependent_majority_matrix() -> pd.DataFrame:
    number_of_coalitions = len(coalitions.ALL)
    majority_matrix = np.zeros((number_of_coalitions, number_of_coalitions))
    idx_x = 0
    idx_y = 0
    for majority_coalition in coalitions.ALL:
        for dependent_coalition in coalitions.ALL:
            majority_matrix[idx_x][idx_y] = calc_dependent_majority(majority_coalition, dependent_coalition)
            idx_y += 1
        idx_x += 1
        idx_y = 0
    party_names = [coalition.name for coalition in coalitions.ALL]
    majority_matrix_as_df = pd.DataFrame(majority_matrix, columns=party_names, index=party_names)
    return majority_matrix_as_df


if __name__ == '__main__':
    polling_results = load_polling_results()
    polls = aggregate(polling_results)
    drift = determine_drift()
    update_parties(polls, drift)
    simulation = simulate_elections()
    seats_by_coalition = calc_seats_by_coalition()
    has_majority_by_coalition = calc_has_majority_by_coalition()

    dependent_majority = calc_dependent_majority(coalitions.BLACK_GREEN, coalitions.GREEN_RED_RED)
    print(dependent_majority)

    dependent_majority_matrix = calc_dependent_majority_matrix()

    share_of_majority_by_coalition = calc_share_of_majority_by_coalition()
    print(share_of_majority_by_coalition)

    share_with_any_majority_by_party = calc_share_with_any_majority_by_party()
    print(share_with_any_majority_by_party)

    share_with_no_majority = calc_share_with_no_majority()
    print(share_with_no_majority)

    probability_hurdle_surpassing = calc_probability_hurdle_surpassing()
    print(probability_hurdle_surpassing)

    coalition_correlation = calc_coalition_correlation(seats_by_coalition)
    
    plotting.plot_seats_by_coalitions(seats_by_coalition)
    plotting.plot_correlation(dependent_majority_matrix)
    plotting.plot_correlation(coalition_correlation)
