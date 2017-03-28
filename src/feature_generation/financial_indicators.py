#!/usr/bin/env python3

"""This module provides many commonly used financial indicators.financial

The design of the classes has to be in line with the base classes from sklearn.
Then, the classes can be used as parts of scikit-learn pipeline.

"""

import pandas as pd

from sklearn.base import TransformerMixin


class MovingAverages(TransformerMixin):

    def __init__(self, windows=[20, 50]):
        self.windows = windows

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        # Construct container
        x_transformed = pd.DataFrame()
        # Construct moving averages
        for i, window in enumerate(self.windows):
            pd.concat([x, x_transformed,
                       pd.Series(x.rolling(window=window).mean(),
                                 name='MA_{}'.format(window))], axis=1)

        x_transformed.fillna(value=0, inplace=True)

        return x_transformed


class LaggedTerms(TransformerMixin):

    def __init__(self, number_of_lags=5):
        self.number_of_lags = number_of_lags

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        pass
