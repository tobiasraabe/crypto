#!/usr/bin/env python3

"""This module provides an moving average crossover strategy.

"""

import numpy as np
import pandas as pd

from .base import BasePredictionModel


class MovingAverage(BasePredictionModel):

    def __init__(self):
        self.y = None
        self.ma_fast = None
        self.ma_slow = None
        self.regimes = None
        self.signals = None

    def fit(self, y, window_fast=12 * 24 * 20, window_slow=12 * 24 * 50):
        """The fit method calculates the moving averages, identifies regimes
        (bearish or bullish periods), and calculates signals.

        Note
        ----
        The default values for the windows are chosen to match a time series
        with five minute intervals. To create a 20-day moving average, one has
        to consider 12 * 24 * 20 observations.

        Arguments
        ---------
        window_fast : int
            Integer indicating the length of the first moving average
        window_slow : int
            Integer indicating the length of the second moving average

        Todo
        ----
        - Find a better solution to fix the problems of integer NaNs than -2

        """
        self.y = y
        # Calculate rolling means
        self.ma_fast = self.y.rolling(window=window_fast).mean()
        self.ma_slow = self.y.rolling(window=window_slow).mean()
        # Assert that there is enough data available
        assert window_fast < window_slow, (
            'The interval of the first moving average is bigger than the'
            'second interval')
        assert y.shape[0] > window_slow, (
            'The interval of the second moving average is larger than the'
            'data.')
        # Vectorized if-else condition to calculate bullish or bearish periods
        self.regimes = np.where(self.ma_fast - self.ma_slow > 0, 1, 0)
        # Vector containing signals to buy, halt, sell (1, 0, -1)
        self.signals = self.regimes - np.roll(self.regimes, 1)
        # np.roll places the last values at the beginning which has no meaning
        # in this case. It would be better to cast the values to np.NaN, but
        # that is not allowed in integer arrays. Therefore, we will use -2.
        self.signals[:1] = -2

        return self

    def predict(self):
        """The method returns an array of signals which states an action.

        Notes
        -----
        The values in ``self.signals`` take the form of three different values.
        -1 stands for a bearish period and calls for selling. 0 means that the
        trade position should be hold and 1 indicates a bullish period, meaning
        buying.

        Return
        ------
        self.signals : array
            Array of signals for trade actions

        """
        return self.signals

    def evaluate(self):
        """This method calculates the percentage of returns for the calculated
        signals.

        Todo
        ----
        I do not know whether this function should be placed here or else.
        Maybe we should better refactor every evaluations.

        Return
        ------
        cum_returns : float
            Float indicating the sum of returns for trades by signals

        """
        # Focus on trades (np.array([BTC_POT_CLOSE, SIGNALS]))
        trades = np.array([
            self.y.loc[(self.signals == -1) | (self.signals == 1)],
            self.signals[(self.signals == -1) | (self.signals == 1)]
        ])
        # Calculates returns
        returns = (trades[0] - np.roll(trades[0], 1)) / trades[0]
        # Use only returns on sells and calculate sum
        cum_returns = sum(returns[trades[1] == -1])

        return cum_returns
