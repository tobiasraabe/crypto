#!/usr/bin/env python3

"""This module provides many commonly used financial indicators.financial

The design of the classes has to be in line with the base classes from sklearn.
Then, the classes can be used as parts of scikit-learn pipeline.

"""

import numpy as np

from sklearn.base import TransformerMixin
from ..utils.statistics import moving_average


class MovingAverages(TransformerMixin):
    """

    Todo
    ----
    - Find better replacement of ``np.NaN`` in :func:`def transform` than 0

    """

    def __init__(self, windows=[20, 50]):
        self.windows = windows

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        # Initialise container
        a = np.empty(self.windows)
        # Create moving averages
        for i, window in enumerate(self.windows):
            a[i] = moving_average(x, window=window)
        # Convert ``np.NaN`` to numerics
        a = np.nan_to_num(a)

        return a


class LaggedTerms(TransformerMixin):

    def __init__(self, number_of_lags=5):
        self.number_of_lags = number_of_lags

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        pass
