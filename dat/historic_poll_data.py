import pandas as pd

data_types = {'Union': float, 'SPD': float, 'Gruene': float, 'FDP': float, 'Linke': float, 'AFD': float,
              'Other': float, 'Total': float, 'Institute': str}

historic_poll_data = pd.read_csv('../dat/historic_poll_data.csv', sep=';', index_col=0, parse_dates=[0], dayfirst=True,
                                 na_values=['–', '?'], thousands=r'.', dtype=data_types, decimal=',')

historic_poll_data = historic_poll_data.sort_index()