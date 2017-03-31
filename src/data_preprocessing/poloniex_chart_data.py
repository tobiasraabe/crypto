#!/usr/bin/env python

import datetime
import pandas as pd
import sys

from bld.project_paths import project_paths_join as ppj
from sklearn.externals import joblib


def dateparse(time_in_secs):
    return datetime.datetime.fromtimestamp(float(time_in_secs))


def main(key: str):
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

    # Make column names uppercase and append key
    ts.columns = map(str.upper, ts.columns)
    ts = ts.add_prefix('{}_'.format(key))

    # Save dataset
    joblib.dump(
        ts, filename=ppj('OUT_DATA_PROCESSED', key + '_chart_data.p.lzma'),
        compress=('lzma', 3))


if __name__ == '__main__':
    key = sys.argv[1]

    main(key)
