#!/usr/bin/env python

import numpy as np
import os
import pytest

from src.data_collection.Poloniex import poloniex_data


def test_init():
    with pytest.raises(TypeError):
        poloniex_data.PoloniexDataManager()


@pytest.fixture(scope='function')
def mock_retry_request(monkeypatch, request):
    monkeypatch.setattr(
        'src.data_collection.Poloniex.poloniex_data.retry_request',
        lambda func: lambda *args, **kwargs: request.param.pop(0)
    )


@pytest.fixture(scope='function')
def manager(monkeypatch, request):
    monkeypatch.setattr(
        'src.data_collection.Poloniex.poloniex_data.END_DATE',
        request.param[0])
    polo = poloniex_data.PoloniexDataManager('BTC_POT')
    polo.start = 0
    polo.period = request.param[1]
    return polo


@pytest.mark.parametrize('manager,mock_retry_request,expected', [
    ((10, 10), [np.arange(10000)], 10),
    ((10, 20), [np.arange(10000), np.arange(10000)], 10),
    ((30000000, 28000000), [np.arange(10000), np.arange(10000)], 25920000),
    ((10, 5), [[], np.arange(10000)], 5),
    ((10, 3), [np.arange(4000), np.arange(8000)], 9),
    ((20, 10), [np.arange(50001), np.arange(25000)], 5)
], indirect=['manager', 'mock_retry_request'])
def test_validate_period(manager, mock_retry_request, expected):
    assert manager.validate_period() == expected


if __name__ == '__main__':
    pytest.main([os.path.join(
        '..', 'src', 'data_collection', 'Poloniex', 'test_poloniex_data.py')])