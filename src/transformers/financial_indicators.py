#!/usr/bin/env python3

"""This module provides many commonly used financial indicators.financial

The design of the classes has to be in line with the base classes from sklearn.
Then, the classes can be used as parts of scikit-learn pipeline.

"""

import numpy as np

from sklearn.base import TransformerMixin
from ..utils.statistics import moving_average


class MovingAverages(TransformerMixin):
    """This class implements a *scikit-learn* transformer class which will
    produce moving averages for a given ``x``.

    Todo
    ----
    - Find better replacement of ``np.NaN`` in :func:`def transform` than 0

    """

    def __init__(self, windows=[20, 50]):
        self.windows = windows

    def fit(self, x, y=None):
        """Since this method needs no fitting, this function is almost empty.
        ``return self`` allows to use a
        `*Fluent Interface* https://en.wikipedia.org/wiki/Fluent_interface`_.
        Note that you have to provide an array.


        Parameters
        ----------
        x : matrix/array
            Data which will be transformed


        Example
        -------
        A fluent interface ensures that ``ma`` after calling ``ma.fit()`` is
        not ``None``:
        ````
        >>> ma = MovingAverages()
        >>> ma = ma.fit()
        >>> print(ma)
        <src.prediction_models.moving_average.MovingAverage object at 0x00000>
        ````

        """
        return self

    def transform(self, x, y=None):
        # Initialise container
        a = np.empty(self.windows)
        # Check whether a matrix or an array is passed and create moving
        # aveages
        if x.ndim == 1:
            for i, window in enumerate(self.windows):
                a[i] = moving_average(x, window=window)
        else:
            for i, x_ in enumerate(x):
                for j, window in enumerate(self.windows):
                    a[i][j] = moving_average(x_, window=window)
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
