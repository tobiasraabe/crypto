#!/usr/bin/env python

import sys
import pandas as pd

from bld.project_paths import project_paths_join as ppj


def main(key: str):
    # Load dataset
    ts_chart = pd.read_pickle(
        ppj('OUT_DATA_PROCESSED', '{}_chart_data.p'.format(key)))
    ts_trade = pd.read_pickle(
        ppj('OUT_DATA_PROCESSED', '{}_trade_history.p'.format(key)))

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
    ts.to_pickle(ppj('OUT_DATA_PROCESSED', '{}.p'.format(key)))


if __name__ == '__main__':
    key = sys.argv[1]

    main(key)
