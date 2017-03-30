#!/usr/bin/env python3

"""This module outputs return values for different moving averages.

"""

import matplotlib.pyplot as plt
import seaborn
import sys

from bld.project_paths import project_paths_join as ppj
from sklearn.externals import joblib
from src.prediction_models.moving_average import MovingAverage
from src.metrics.scorer import moving_average_score


if __name__ == '__main__':
    key = sys.argv[1]
    fast = int(sys.argv[2])
    slow = int(sys.argv[3])

    data = joblib.load(
        ppj('OUT_DATA_PROCESSED', '{}_chart_data.p.lzma'.format(key)))
    y = data.BTC_POT_CLOSE

    ma = MovingAverage()
    ma = ma.fit(y=y, window_fast=fast, window_slow=slow)
    results = ma.predict()
    moving_average_score(y, results)

    # Generate graphics for regimes, signals, profits
