#!/usr/bin/env python3

import numpy as np
import pandas as pd
import pytest

from numpy.testing import assert_array_almost_equal

# Import functions which are tested
from .statistics import moving_average


@pytest.mark.parametrize('array,window', [
    (np.arange(50), 10),
    (np.arange(1000), 50),
    (np.linspace(0, 1, 123456789), 1000)
])
def test_moving_average(array, window):
    assert None is assert_array_almost_equal(
        pd.Series(array).rolling(window=window).mean(),
        moving_average(array, window))
