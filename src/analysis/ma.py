#!/usr/bin/env python3

"""This module outputs return values for different moving averages.

"""

import matplotlib.pyplot as plt
import seaborn  # noqa: F401
import sys

from bld.project_paths import project_paths_join as ppj
from collections import OrderedDict
from sklearn.externals import joblib
from src.metrics.scorer import moving_average_score
from src.prediction_models.moving_average import MovingAverage


def create_price_trade_graph(trades, prices, key, fast, slow, score):
    fig = plt.figure()
    fig.suptitle('Prices and Trade Outcomes, Score: {0:6f}'.format(score))
    plt.plot(prices, label=key)
    for row in trades.iterrows():
        label = 'Gain' if row[1]['RETURNS'] > 0 else 'Loss'
        color = 'green' if row[1]['RETURNS'] > 0 else 'red'
        plt.plot(
            [row[1]['FROM'], row[1]['TO']],
            [row[1]['BTC_POT_FROM'], row[1]['BTC_POT_TO']],
            'k-', lw=2, color=color, label=label)

    # Remove duplicates from legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.savefig(ppj('OUT_FIGURES', 'ma_price_{}_{}_{}.png'
                    .format(key, fast, slow)))


def create_regime_signal_graph(df, key, fast, slow):
    fig, ax = plt.subplots(2, 1)
    fig.suptitle('Regimes and Signals')

    ax1 = plt.subplot(2, 1, 1)
    plt.plot(df.SIGNALS)
    ax1.set_title('Signals')

    ax2 = plt.subplot(2, 1, 2)
    plt.plot(df.REGIMES)
    ax2.set_title('Regimes')
    plt.savefig(ppj('OUT_FIGURES', 'ma_signal_regime_{}_{}_{}.png'
                    .format(key, fast, slow)))


if __name__ == '__main__':
    key = sys.argv[1]
    fast = int(sys.argv[2])
    fast_adj = fast * 12 * 24
    slow = int(sys.argv[3])
    slow_adj = slow * 12 * 24

    data = joblib.load(
        ppj('OUT_DATA_PROCESSED', '{}_chart_data.p.lzma'.format(key)))
    y = data.BTC_POT_CLOSE

    ma = MovingAverage()
    ma = ma.fit(y=y, window_fast=fast_adj, window_slow=slow_adj)
    results = ma.predict()
    score = moving_average_score(y, results)

    # Generate graphics for regimes, signals, profits
    # Prepare data
    plot = y.to_frame()
    plot['SIGNALS'] = ma.signals
    plot['REGIMES'] = ma.regimes
    create_regime_signal_graph(plot, key, fast,
                               slow)

    trades = plot.BTC_POT_CLOSE[
        (plot.SIGNALS == -1) | (plot.SIGNALS == 1)].reset_index()
    trades.rename(
        columns={'date': 'FROM', 'BTC_POT_CLOSE': 'BTC_POT_FROM'},
        inplace=True)
    trades['RETURNS'] = (
        (trades.BTC_POT_FROM - trades.BTC_POT_FROM.shift(1)) /
        trades.BTC_POT_FROM)
    trades['BTC_POT_TO'] = trades.BTC_POT_FROM.shift(1)
    trades['TO'] = trades.FROM.shift(1)
    trades = trades[trades.index % 2 != 0]
    create_price_trade_graph(
        trades, plot.BTC_POT_CLOSE, key, fast,
        slow, score)
