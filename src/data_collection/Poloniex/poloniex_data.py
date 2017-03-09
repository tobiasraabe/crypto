#!/usr/bin/env python

import datetime
import os
import pandas as pd
import poloniex
import requests
import sys
import time
import yaml

from bld.project_paths import project_paths_join as ppj

# Use UTC unix time stamp
END_DATE = int(datetime.datetime.utcnow().timestamp())
DELAY = 1


def retry_request(func):
    """Decorator which repeats an API call with ``requests`` in case of an
    ``requests.exceptions.ReadTimeout``.

    The reason is that requests operation from poloniex sometimes fail, but
    rerunning the command yields the correct return.

    There are at most five times to receive a valid return.


    Parameters
    ----------
    func : function
        Wrapped function using requests

    """

    def wrap(*args, **kwargs):
        i = 0
        while i <= 4:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.ReadTimeout:
                i += 1
                time.sleep(DELAY)
                pass
            else:
                break
    return wrap


class PoloniexDataManager:
    """This class offers the ability to collect data from the public API of
    Poloniex.


    Parameters
    ----------
    key : str
        Poloniex identifier of an exchange

    Attributes
    ----------
    multiplicator : int
        Multiplicator for ``self.period`` which adds a constant upward
        push.

        Since trades on Poloniex are not constant but highly volatile,
        ``self.period`` would be too short after a period with unusually
        many trades. The multiplier helps the interval to regenerate.

    path_config_main : str
        Path to the main configuration file. Each key in the configuration
        represents a currency pair which has a ``START_DATE`` and a
        ``PERIOD``::

            <key>:
              START_DATE: <int>
              PERIOD: <int>


    Yields
    ------
    <key>_trade_history.csv :
        CSV-file comprising the trade history for a given key
    <key>_chart_data_csv :
        CSV-file comprising the chart data for a given key

    """
    multiplicator = 1.1
    path_config_main = ppj(
        'IN_DATA_COLLECTION', 'Poloniex', 'poloniex_config.yml')

    def __init__(self, key):
        """
        Attributes
        ----------
        key : str
            Poloniex identifier of a currency pair
        path_config_temp : str
            Path to temporary configuration for a key
        period : int
            Time interval in unix time
        start : int
            Start point in unix time

        """

        self.key = key
        self.path_config_temp = ppj('OUT_DATA_RAW', self.key + '.yml')

        self.period = None
        self.start = None

    def generate_trade_history(self):
        """Wraps the entire process of generating the trade history.


        """

        # Load configuration
        try:
            with open(self.path_config_temp) as file:
                config_temp = yaml.load(file.read())
                self.start = config_temp['trade_history']['END_DATE']
                self.period = config_temp['trade_history']['PERIOD']
        except FileNotFoundError:
            with open(self.path_config_main) as file:
                config_main = yaml.load(file.read())
            self.start = config_main[self.key]['START_DATE']
            self.period = config_main[self.key]['PERIOD']

        # Collect data
        print('START: Generating data for {} - Trade History.'
              .format(self.key))
        while True:
            self.period = self.validate_period(self.multiplicator)
            self.gen_th()
            self.start += self.period
            if self.start == END_DATE:
                break

        # Save new configuration
        try:
            with open(ppj('OUT_DATA_RAW', '{}.yml'
                          .format(self.key)), 'r+') as file:
                temp = yaml.load(file.read())
                if temp is None:
                    raise FileNotFoundError
                temp.update(
                    {'trade_history':
                     {'END_DATE': self.start, 'PERIOD': self.period}
                     })
                yaml.dump(temp, file)
        except FileNotFoundError:
            with open(ppj('OUT_DATA_RAW', '{}.yml'
                          .format(self.key)), 'w') as file:
                yaml.dump(
                    {'trade_history':
                     {'END_DATE': self.start, 'PERIOD': self.period}
                     }, file)

        print('SUCCESS: Created {} - Trade History'.format(self.key))

    def generate_chart_data(self):
        """Wraps the entire process of generating chart data.

        """

        # Load configuration
        try:
            with open(self.path_config_temp) as file:
                config_temp = yaml.load(file.read())
                self.start = config_temp['chart_data']['END_DATE']
        except (FileNotFoundError, KeyError):
            with open(self.path_config_main) as file:
                config_main = yaml.load(file.read())
            self.start = config_main[self.key]['START_DATE']

        # Collect data
        print('START: Generating data for {} - Chart Data'
              .format(self.key))
        self.gen_cd()

        # Save new configuration
        try:
            with open(ppj('OUT_DATA_RAW', '{}.yml'
                          .format(self.key)), 'r+') as file:
                temp = yaml.load(file.read())
                if temp is None:
                    raise FileNotFoundError
                temp.update({'chart_data': {'END_DATE': self.start}})
                yaml.dump(temp, file)
        except FileNotFoundError:
            with open(ppj('OUT_DATA_RAW', '{}.yml'
                          .format(self.key)), 'w') as file:
                yaml.dump({'chart_data': {'END_DATE': END_DATE}}, file)

        print('SUCCESS: Created {} - Chart Data'.format(self.key))

    def validate_period(self, multiplicator=1) -> int:
        """The function validates the period for an API call.

        The main problem is that an API call can only return up to 50,000
        items. A constant period cannot adjust to the increasing trade volume
        of Poloniex. Also, invalid API outputs are handled here.


        Notes
        -----
        If the function corrects ``self.period``, it checks the new
        value recursively.

        A constant upward push is applied to overcome too small
        ``self.period``.

        The part of the code which is responsible for checking the number of
        output elements and adjusting the period uses a simple algorithm to
        adjust ``self.period``.


        Todo
        ----
        - Is there general solution for adjusting the period?


        Parameters
        ----------
        multiplicator : int
            Constant upward push to ``self.period``


        Returns
        -------
        period : int
            Period in unix time

        """

        self.period = int(self.period * multiplicator)

        polo = poloniex.Poloniex()

        api_out = retry_request(polo.marketTradeHist)(
            self.key, start=self.start, end=self.start + self.period)

        # print('Pair: {}, Start: {}, Period: {}, End: {}, Left: {},'
        #       ' No. items: {}'
        #       .format(self.key, self.start, self.period,
        #               self.start + self.period,
        #               END_DATE - self.start - self.period, len(api_out)))

        time.sleep(DELAY)

        # Algorithm to adjust ``self.period``
        if self.start + self.period == END_DATE:
            return self.period

        elif self.start + self.period > END_DATE:
            print('WARNING: REACHED END_DATE')
            self.period = END_DATE - self.start
            return self.validate_period()

        elif self.period > 2592000 * 10:
            print('WARNING: REACHED MAXIMUM PERIOD')
            self.period = 2592000 * 10
            return self.validate_period()

        elif type(api_out) is dict:
            print('ERROR: FATAL ERROR')
            sys.exit(1)

        elif len(api_out) == 0:
            print('WARNING: EMPTY LIST WAS RETURNED')
            self.start += self.period
            return self.validate_period()

        elif len(api_out) < 5000:
            print('WARNING: INTERVAL IS TOO SMALL')
            self.period *= 3
            return self.validate_period()

        elif len(api_out) >= 50000:
            print('ERROR: INTERVAL IS TOO LONG')
            self.period = int(self.period * 0.5)
            return self.validate_period()

        else:
            return self.period

    def gen_th(self):
        """Handles the return from a valid API call to get the trade history
        and appends the data to an existing file or creates a new one.

        """

        polo = poloniex.Poloniex()
        path_data = ppj(
            'OUT_DATA_RAW', self.key + '_trade_history.csv')

        df = pd.DataFrame(
            retry_request(
                polo.marketTradeHist)(
                self.key, start=self.start, end=self.start + self.period)
        )

        time.sleep(DELAY)

        if os.path.isfile(path_data):
            header_bool = False
            print('SUCCESS: DATA WAS APPENDED')
        else:
            header_bool = True
            print('SUCCESS: DATASET WAS CREATED')
        with open(path_data, 'a') as file:
            df.to_csv(
                file, index=False, header=header_bool, columns=df.columns)

    def gen_cd(self):
        """Handles the return from a valid API call to get the chart data
        and appends the data to an existing file or creates a new one.

        """

        polo = poloniex.Poloniex()
        path_data = ppj('OUT_DATA_RAW', self.key + '_chart_data.csv')

        df = pd.DataFrame(
            retry_request(
                polo.returnChartData)(
                self.key, period=300, start=self.start, end=END_DATE)
        )

        time.sleep(DELAY)

        if os.path.isfile(path_data):
            header_bool = False
            print('Data was appended')
        else:
            header_bool = True
            print('Dataset was created.')
        with open(path_data, 'a') as file:
            df.to_csv(
                file, index=False, header=header_bool, columns=df.columns)

    def __call__(self):
        self.generate_trade_history()
        self.generate_chart_data()


if __name__ == '__main__':
    key = sys.argv[1]

    PoloniexDataManager(key)()
