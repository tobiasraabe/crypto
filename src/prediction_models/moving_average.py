#!/usr/bin/env python3

"""Moving averages (MA) are widely used indicators in technical analysis that
help smooth out price action by filtering out the noise from random price
fluctuations. A moving average is a trend-following or lagging indicator
because it is based on past prices. The two basic and commonly used MAs are the
simple moving average (SMA), which is the simple average of a security over a
defined number of time periods, and the exponential moving average (EMA), which
gives bigger weight to more recent prices. The most common applications
of MAs are to identify the trend direction and to determine support and
resistance levels. While MAs are useful enough on their own, they also
form the basis for other indicators such as the Moving Average Convergence
Divergence (MACD).

"""

import numpy as np

import warnings

from ..utils.statistics import moving_average
from .base import BasePredictionModel


class MovingAverage(BasePredictionModel):
    """This class provides an estimator which uses moving average crossover
    strategy with two moving averages where one is considered faster than the
    other (e.g. a 20-day and a 50-day MA). This is because the MA with the
    bigger interval is more robust to present price changes than the other.

    Both averages will give indicators on when it is profitable to buy and to
    sell. An indicator to sell is if the 20-day MA crosses the 50-day MA from
    below and an indicator to sell if the 20-day MA crosses the 50-day MA from
    above.

    The indicators are called signals and are returned by the estimator with
    the ``predict()`` method.


    Attributes
    ----------
    y : pd.Series/np.array
        An array of prices
    ma_fast : np.array
        An array containing the MA with smaller interval
    ma_slow : np.array
        An array containing the MA with bigger interval
    regimes : np.array
        A vectorized if-else condition with 1 for ``ma_fast > ma_slow`` and 0
        for ``ma_fast <= ma_slow``
    signals : np.array
        An array of signals where 1 calls for buying and -1 for selling


    """

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
        signals : np.array
            An array of signals where 1 calls for buying and -1 for selling

        """
        return self.signals
