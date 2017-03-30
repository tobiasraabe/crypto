#!/usr/bin/env python3

"""This module outputs return values for different moving averages.

"""

import matplotlib.pyplot as plt
import seaborn
import sys

from bld.project_paths import project_paths_join as ppj
from sklearn.externals import joblib
from src.prediction_models.long_short_term import Lstm
from src.prediction_models.scorer import portfolio_score


if __name__ == '__main__':
    key = sys.argv[1]
    layers = int(sys.argv[2])
    trans_type = str(sys.argv[3])
    lags = int(sys.argv[4])
    reduce = int(sys.argv[5])
    iterations = int(sys.argv[6])

    df = joblib.load(
        ppj('OUT_DATA_PROCESSED','{}_trade_history.p.lzma'.format(key)))

    longstm = Lstm()
    lstmresults = longstm.fit(df,layers,trans_type,lags,reduce,
                              iterations)

    portfolio_score(lstmresults)

