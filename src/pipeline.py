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


if __name__ == '__main__':
    polling_results = load_polling_results()
    polls = aggregate(polling_results)
    drift = determine_drift()
    update_parties(polls, drift)
    simulation = simulate_elections()
    print(simulation)
    plotting.plot_coalitions(simulation)

    # TODO: still to implement
    #evaluate_five_percent_hurdle()
    #make_plots()
    #evaluation_coalition_correlation()
