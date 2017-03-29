#!/usr/bin/env python3

"""This module contains helper functions to calculate statistics.

"""

import numpy as np


def moving_average(array, window: int) -> np.array:
    """This functions calculates an moving average and is an attempt to emulate
    ``pd.Series.rolling().mean()``.

    Parameters
    ---------
    values : arr
        Values for which an moving average is calculated
    windows : int
        Interval for moving average

    Example
    -------
    >>> array = np.array([1, 2, 3, 4, 5])
    >>> moving_average(array, 3)
    array([np.NaN, np.NaN, 2, 3, 4])

    Note that the first two elements of the array are of type ``np.NaN`` since
    the moving average is calculated for an interval of 3 (``window``) values
    ending at the input position. The first and second element do not have a
    complete series of 3 elements which converts them to ``np.NaN``.

    """
    weights = np.repeat(1.0, window) / window
    sma = np.convolve(array, weights, 'valid')

    return np.append([np.nan] * (window - 1), sma)
