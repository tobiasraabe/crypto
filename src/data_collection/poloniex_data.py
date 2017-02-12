import os
import sys
import pandas as pd
import time
from bld.project_paths import project_paths_join as ppj
import yaml
import poloniex
import datetime

# Use UTC unix time stamp
END_DATE = int(datetime.datetime.utcnow().timestamp())


def validate_period(pair: str, start: int, period: int) -> int:
    """The function validates the period for an API call.

    The main problem is that an API call can only return up to 50,000 items.
    A constant period cannot adjust to the increasing trade volume of
    Poloniex. Also, invalid API outputs are handled here.

    Note that, if the function corrects ``period``, it checks the new value
    recursively.

    Parameters
    ----------
    pair : str
        Exchange key
    start: int
        Start in unix time
    period : int
        Period in unix time

    Returns
    -------
    period : int
        Period in unix time

    """

    polo = poloniex.Poloniex()
    api_out = polo.marketTradeHist(pair, start=start, end=start + period)

    print('Pair: {}, Start: {}, Period: {}, End: {}, Left: {}, No. items: {}'
          .format(pair, start, period, start + period,
                  END_DATE - start - period, len(api_out)))
    time.sleep(1)

    if start + period == END_DATE:
        return period
    elif start + period > END_DATE:
        return validate_period(pair, start, END_DATE - start)
    elif period > 2592000 * 10:
        return validate_period(pair, start, 2592000 * 10)
    elif type(api_out) is dict:
        print('ERROR: FATAL ERROR')
        sys.exit(1)
    elif len(api_out) == 0:
        print('WARNING: Empty list was returned')
        return validate_period(pair, start + period, period)
    elif len(api_out) < 5000:
        print('WARNING: Interval is too small')
        return validate_period(pair, start, int(period * 3))
    elif len(api_out) >= 50000:
        print('ERROR: Interval is too long.')
        return validate_period(pair, start, int(period * 0.5))
    else:
        return period


def generate_data(pair: str, start: int, period: int):
    """Recieves a valid API call and writes ``DataFrame`` to disk.

    Parameters
    ----------
    pair : str
        Exchange key
    start: int
        Start in unix time
    period : int
        Period in unix time

    """

    path_data = ppj('OUT_DATA_RAW', pair + '_temp.csv')
    polo = poloniex.Poloniex()

    df = pd.DataFrame(polo.marketTradeHist(pair, start=start,
                                           end=start + period))

    time.sleep(1)

    if os.path.isfile(path_data):
        header_bool = False
        print('Data was appended')
    else:
        header_bool = True
        print('Dataset was created.')
    with open(path_data, 'a') as file:
        df.to_csv(file, index=False, header=header_bool, columns=df.columns)


def clean_data(pair: str):
    """Cleans the dataset after generation.

    Parameters
    ----------
    pair : str
        Period in unix time

    """

    path_data = ppj('OUT_DATA_RAW', pair + '_temp.csv')
    df = pd.read_csv(path_data, index_col=0)

    df.drop_duplicates(subset='globalTradeID', inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('globalTradeID', inplace=True)

    path_data = ppj('OUT_DATA_RAW', pair + '.csv')
    df.to_csv(path_data)


if __name__ == '__main__':
    pair = sys.argv[1]
    with open(ppj('IN_DATA_COLLECTION', 'poloniex_config.yml')) as file:
        polo_config = yaml.load(file.read())

    try:
        with open(ppj('OUT_DATA_RAW', '{}.yml'.format(pair))) as file:
            config = yaml.load(file.read())
    except FileNotFoundError:
        start = polo_config['START_DATE']
        period = polo_config['PERIOD']
    else:
        start = int(config['start'])
        period = int(config['period'])

    print('START: Generating data for {}.'.format(pair))
    while True:
        period = validate_period(pair, start, period)
        generate_data(pair, start, period)
        start = start + period
        if start == END_DATE:
            break

    clean_data(pair)
    with open(ppj('OUT_DATA_RAW', '{}.yml'.format(pair)), 'w') as file:
        yaml.dump({'start': start, 'period': period}, file)
    print('SUCCESS: Created {} dataset'.format(pair))
