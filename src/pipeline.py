import pandas as pd

from dat.loader import Loader
from simulation import Simulation
import parties
import coalitions


def load_polling_results():
    loader = Loader()
    polls_by_party = [loader.get_latest_percentages_of(party) for party in parties.ALL]
    dates = loader.get_latest_dates_of_polls()
    df = pd.DataFrame.from_records(polls_by_party).T
    df.columns = [party.name for party in parties.ALL]
    df.index = dates
    return df



if __name__ == '__main__':
    load_polling_results()
    #aggregate_polls()
    #simulate_elections()
    #evaluation_coalitions()
    #evaluate_five_percent_hurdle()
    #make_plots()
    #evaluation_coalition_correlation()
