#!/usr/bin/env python3

import numpy as np
import pytest

from numpy.testing import assert_array_almost_equal
from src.transformers.financial_indicators import MovingAverages
from src.utils.statistics import moving_average


@pytest.fixture(scope='function')
def ma_class():
    return MovingAverages(windows=[20])


@pytest.mark.skip(reason='Need better programmers :)')
@pytest.mark.parametrize('array,windows', [
    (np.arange(25), [20]),
    (np.arange(100), [20])
    # (np.array([np.arange(25), np.arange(25)]), [20])  # Currently, no matrix
])
def test_MovingAverage(ma_class, array, windows):
    ma = ma_class
    ma = ma.fit(array)
    ma = ma.transform(array)

    for window in windows:
        for i, arr in enumerate(array):
            assert None is assert_array_almost_equal(
                ma[i], np.nan_to_num(moving_average(arr, window)))
            assert not np.isnan(ma).any()
