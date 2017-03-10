#!/usr/bin/env python

import pandas as pd
import sys

from bld.project_paths import project_paths_join as ppj
from sklearn.externals import joblib


def main(key: str):
    """Merges chart data and trade history for a given currency pair.

    Parameters
    ----------
    key : str
        Poloniex identifier of a currency pair

    Yields
    ------
    ts : pd.DataFrame
        Pickled and compressed DataFrame

    """

    # Load dataset
    ts_chart = joblib.load(
        ppj('OUT_DATA_PROCESSED', '{}_chart_data.p.lzma'.format(key)))
    ts_trade = joblib.load(
        ppj('OUT_DATA_PROCESSED', '{}_trade_history.p.lzma'.format(key)))

    # Change column names
    ts_chart.columns = map(str.upper, ts_chart.columns)
    ts_chart['CHART'] = True

    ts_trade.columns = map(str.upper, ts_trade.columns)
    ts_trade['TRADE'] = True

    # Merge datasets
    ts = ts_chart.join(ts_trade, how='outer')

    # Fill NaNs
    ts.CHART.fillna(False, inplace=True)
    ts.TRADE.fillna(False, inplace=True)

    # Save dataset
    joblib.dump(
        ts, filename=ppj('OUT_DATA_PROCESSED', '{}.p.lzma'.format(key)),
        compress=('lzma', 3))


if __name__ == '__main__':
    key = sys.argv[1]

    main(key)
