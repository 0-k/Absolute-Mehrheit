import pandas as pd

data_types = {'Union': float, 'SPD': float, 'Gruene': float, 'FDP': float, 'Linke': float, 'AFD': float,
              'Other': float, 'Total': float, 'Institute': str}

data = pd.read_csv('../data/poll_data_germany.csv', sep=';', index_col=0, parse_dates=[0], dayfirst=True,
                   na_values=['–', '?'], thousands=r'.', dtype=data_types, decimal=',')

data = data.sort_index()
