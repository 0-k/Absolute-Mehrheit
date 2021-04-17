import pandas as pd
from datetime import date

from dat.loader import Loader
from simulation import Simulation
import parties
import coalitions
from src.data_model import PollModel


def load_polling_results():
    loader = Loader()
    polls_by_party = [loader.get_latest_percentages_of(party) for party in parties.ALL]
    dates = loader.get_latest_dates_of_polls()
    df = pd.DataFrame.from_records(polls_by_party).T
    df.columns = [party.name for party in parties.ALL]
    df.index = dates
    df = df.sort_index()
    return df

def aggregate(polls):
    poll_aggregation = PollModel()
    poll_aggregation.data = polls
    poll_aggregation.update_dates(pd.Timestamp(date.today()))
    return poll_aggregation.calc_current_average()




if __name__ == '__main__':
    polling_results = load_polling_results()
    polls_aggregated = aggregate(polling_results)
    #simulate_elections()
    #evaluation_coalitions()
    #evaluate_five_percent_hurdle()
    #make_plots()
    #evaluation_coalition_correlation()
