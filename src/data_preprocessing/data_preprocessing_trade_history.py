#!/usr/bin/env python

import sys
import pandas as pd
import datetime
from bld.project_paths import project_paths_join as ppj


def dateparse(datetime_str):
    return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')


def main(key: str):
    # Load dataset
    ts = pd.read_csv(
        ppj('OUT_DATA_RAW', '{}_trade_history.csv'.format(key)),
        parse_dates=True, index_col='date', date_parser=dateparse)

    # Drop possible duplicates
    ts = ts.loc[~ ts.tradeID.duplicated()]

    # Drop unnecessary columns
    ts.drop(['globalTradeID', 'tradeID'], axis=1, inplace=True)

    # Make column names uppercase and append key
    ts.columns = map(str.upper, ts.columns)
    ts = ts.add_prefix(key)

    # Save as pickle
    ts.to_pickle(
        ppj('OUT_DATA_PROCESSED', '{}_trade_history.p'.format(key)))


if __name__ == '__main__':
    key = sys.argv[1]
    main(key)
