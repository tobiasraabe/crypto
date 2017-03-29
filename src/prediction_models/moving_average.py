#!/usr/bin/env python3

"""This module provides an moving average crossover strategy.

"""

import numpy as np

import warnings

from ..utils.statistics import moving_average
from .base import BasePredictionModel


class MovingAverage(BasePredictionModel):

    def __init__(self):
        self.y = None
        self.ma_fast = None
        self.ma_slow = None
        self.regimes = None
        self.signals = None

    def fit(self, y, window_fast: int = 5, window_slow: int = 10):
        """The fit method calculates the moving averages, identifies regimes
        (bearish or bullish periods), and calculates signals.

        Note
        ----
        The default values for the windows are chosen to match a time series
        with five minute intervals. To create a 20-day moving average, one has
        to consider 12 * 24 * 20 observations.

        Parameters
        ---------
        window_fast : int
            Integer indicating the length of the first moving average
        window_slow : int
            Integer indicating the length of the second moving average

        Todo
        ----
        - Find a better solution to fix the problems of integer NaNs than -2

        """
        # Assert that there is enough data available
        assert window_fast < window_slow, (
            'The interval of the first moving average is bigger than the'
            'second interval')
        assert y.shape[0] > window_slow, (
            'The interval of the second moving average is larger than the'
            'data.')
        # Convert input to pd.Series to make use of rolling mean
        self.y = y
        # Calculate rolling means
        self.ma_fast = moving_average(array=y, window=window_fast)
        self.ma_slow = moving_average(array=y, window=window_slow)
        # Vectorized if-else condition to calculate bullish or bearish periods
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            self.regimes = np.where(self.ma_fast - self.ma_slow > 0, 1, 0)
        # Vector containing signals to buy, halt, sell (1, 0, -1)
        self.signals = self.regimes - np.roll(self.regimes, 1)
        # np.roll places the last values at the beginning which has no meaning
        # in this case. It would be better to cast the values to np.NaN, but
        # that is not allowed in integer arrays. Therefore, we will use -2.
        self.signals[0] = -2

        return self

    def predict(self):
        """The method returns an array of signals which states an action.

        Notes
        -----
        The values in ``self.signals`` take the form of three different values.
        -1 stands for a bearish period and calls for selling. 0 means that the
        trade position should be hold and 1 indicates a bullish period, meaning
        buying.

        Returns
        -------
        self.signals : np.array
            Array of signals for trade actions

        """
        return self.signals
