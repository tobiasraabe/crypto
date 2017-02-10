import os
import sys
import pandas as pd
import time
from bld.project_paths import project_paths_join as ppj
import yaml


FETCH_URL = ('https://poloniex.com/public?command=returnChartData&'
             'currencyPair={0}&start={1}&end={2}&period=300')
COLUMNS = ['date', 'high', 'low', 'open', 'close',
           'volume', 'quoteVolume', 'weightedAverage']
# Date 01/01/2014, Poloniex is founded
START_DATE = 1388530800
# Conversion ensures that the timestamp is exactly on one of the five minute
# updates
END_DATE = int(time.time() / 400) * 400


def get_data(pair: str, start: int, end: int):
    # Adjust strings
    datafile = ppj('OUT_DATA_RAW', pair + '.csv')
    url = FETCH_URL.format(pair, start, end)

    print('Get {} from {} to {}'.format(pair, start, end))

    df = pd.read_json(url, convert_dates=False)

    if df['date'].iloc[-1] == 0:
        print('No data.')
    else:
        with open(datafile, 'a') as file:
            if os.path.isfile(datafile):
                df.to_csv(file, index=False, cols=COLUMNS, header=False)
                print('Data was appended')
            else:
                df.to_csv(file, index=False, cols=COLUMNS)
                return df.loc[0, 'date']
                print('Dataset was created.')


def main(pair: str):
    # If data was downloaded before, load start and end date
    if os.path.isfile(ppj('OUT_DATA_RAW', '{}.yml'.format(pair))):
        with open(ppj('OUT_DATA_RAW', '{}.yml'.format(pair)), 'r') as file:
            config = yaml.load(file.read())
        start = int(config['end']) + 1
    else:
        start = START_DATE

    end = END_DATE
    real_start = get_data(pair, start, end)

    # Prepare new configuration and dump it
    temp = {'start': real_start if real_start is not None else START_DATE,
            'end': end}
    with open(ppj('OUT_DATA_RAW', '{}.yml'.format(pair)), 'w') as file:
        yaml.dump(temp, file, default_flow_style=False)


if __name__ == '__main__':
    pair = sys.argv[1]
    main(pair)
