#!/usr/bin/env python

import datetime
import pandas as pd
import sys
import yaml

from bld.project_paths import project_paths_join as ppj
from sklearn.externals import joblib


def dateparse(time_in_secs):
    return datetime.datetime.fromtimestamp(float(time_in_secs))


def create_lags(ts, lags=1):
    lag = 1
    ts_lagged = pd.DataFrame()
    while lag <= lags:
        ts_shifted = ts.shift(-lag)
        ts_shifted.columns = [
            i + '_lag_{}'.format(lag) for i in ts_shifted.columns]
        ts_lagged = pd.concat([ts_lagged, ts_shifted], axis=1)
        lag += 1
    return ts_lagged.dropna()


def main(key: str, lags: int):
    """Preprocesses the chart data for a given currency pair. Furthermore,
    a number of lags is computed according to the argument.

    Parameters
    ----------
    key : str
        Poloniex identifier of a currency pair
    lags : int
        Number of computed lags

    Yields
    ------
    ts : pd.DataFrame
        Pickled and compressed DataFrame

    """

    # Load dataset
    ts = pd.read_csv(
        ppj('OUT_DATA_RAW', '{}_chart_data.csv'.format(key)), parse_dates=True,
        index_col='date', date_parser=dateparse
    )

    # Remove duplicated rows
    ts = ts[~ ts.index.duplicated()]

    # Create lagged variables
    ts_lagged = create_lags(ts.drop('close', axis=1), lags)

    # Concat lagged independent variables and drop NANs
    ts = pd.concat([ts.close, ts_lagged], axis=1).dropna()

    # Make column names uppercase and append key
    ts.columns = map(str.upper, ts.columns)
    ts = ts.add_prefix('{}_'.format(key))

    # Save dataset
    joblib.dump(
        ts, filename=ppj('OUT_DATA_PROCESSED', key + '_chart_data.p.lzma'),
        compress=('lzma', 3))


if __name__ == '__main__':
    key = sys.argv[1]

    with open(ppj('IN_DATA_PREPROCESSING', 'data_preprocessing.yml')) as file:
        lags = yaml.load(file.read())['LAGS']

    main(key, lags)
