#!/usr/bin/env python
import datetime
import os
import pandas as pd
import poloniex
import sys
import time
import yaml

from bld.project_paths import project_paths_join as ppj

# Use UTC unix time stamp
END_DATE = int(datetime.datetime.utcnow().timestamp())
DELAY = 1


class PoloniexDataManager:
    """This class offers the ability to collect data from the public API of
    Poloniex.

    """

    methods = ['marketTradeHist', 'returnChartData']

    def __init__(self, key, start_date, period):
        self.key = key
        self.path_config = ppj('OUT_DATA_RAW', self.key + '_config.yml')

        try:
            with open(self.path_config) as config_temp:
                self.start = config_temp[self.key]['END_DATE']
                self.period = config_temp[self.key]['PERIOD']
        except FileNotFoundError:
            self.start = start_date
            self.period = period
        finally:
            print('START: Generating data for {}.'.format(self.key))
            for method_name in self.methods:
                while True:
                    self.period = self.validate_period(method_name)
                    self.generate_data(method_name)
                    self.start += self.period
                    if self.start == END_DATE:
                        break

                self.remove_duplicates(method_name)
                with open(ppj('OUT_DATA_RAW', '{}.yml'
                              .format(self.key)), 'r+') as file:
                    temp = yaml.load(file.read())
                    temp[self.key]['END_DATE'] = self.start
                    temp[self.key]['PERIOD'] = self.period
                    yaml.dump(temp, file)
                print('SUCCESS: Created {}-{} dataset'
                      .format(self.key, method_name))

    def validate_period(self, method_name: str) -> int:
        """The function validates the period for an API call.

        The main problem is that an API call can only return up to 50,000
        items. A constant period cannot adjust to the increasing trade volume
        of Poloniex. Also, invalid API outputs are handled here.

        Note that, if the function corrects ``self.period``, it checks the new
        value recursively.

        Parameters
        ----------
        method_name : str
            Name of performed method

        Returns
        -------
        period : int
            Period in unix time

        """
        polo = poloniex.Poloniex()
        method = getattr(polo, method_name)
        api_out = method(
            self.key, start=self.start, end=self.start + self.period)

        print('Pair: {}, Method: {}, Start: {}, Period: {}, End: {}, Left: {},'
              ' No. items: {}'
              .format(self.key, method_name, self.start, self.period,
                      self.start + self.period,
                      END_DATE - self.start - self.period, len(api_out)))

        time.sleep(DELAY)

        if self.start + self.period == END_DATE:
            return self.period

        elif self.start + self.period > END_DATE:
            self.period = END_DATE - self.start
            return self.validate_period(method_name)

        elif self.period > 2592000 * 10:
            self.period = 2592000 * 10
            return self.validate_period(method_name)

        elif type(api_out) is dict:
            print('ERROR: FATAL ERROR')
            sys.exit(1)

        elif len(api_out) == 0:
            print('WARNING: Empty list was returned')
            self.start += self.period
            return self.validate_period(method_name)

        elif len(api_out) < 5000:
            print('WARNING: Interval is too small')
            self.period *= 3
            return self.validate_period(method_name)

        elif len(api_out) >= 50000:
            print('ERROR: Interval is too long.')
            self.period = int(self.period * 0.5)
            return self.validate_period(method_name)

        else:
            return self.period

    def generate_data(self, method_name: str):
        """Recieves a valid API call and writes ``DataFrame`` to disk.

        Parameters
        ----------
        pair : str
            Exchange key

        """
        polo = poloniex.Poloniex()
        method = getattr(polo, method_name)
        path_data = ppj(
            'OUT_DATA_RAW', self.key + '_' + method_name + '.csv')

        df = pd.DataFrame(method(
            self.key,
            start=self.start,
            end=self.start + self.period)
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

    def remove_duplicates(self, method_name: str):
        """Cleans the dataset after generation.

        """
        if method_name == 'trade_history':
            subset = 'globalTradeID'
        elif method_name == 'chart_data':
            subset = 'date'

        path_data = ppj(
            'OUT_DATA_RAW', self.key + '_' + method_name + '.csv')
        df = pd.read_csv(path_data, index_col=0)

        df.drop_duplicates(subset=subset, inplace=True)
        df.sort_values(subset, axis=1, inplace=True)

        path_data = ppj(
            'OUT_DATA_RAW', self.key + '_' + method_name + '.csv')
        df.to_csv(path_data)


if __name__ == '__main__':
    key = sys.argv[1]

    with open(ppj('IN_DATA_COLLECTION', 'Poloniex',
                  'poloniex_config.yml')) as file:
        config_main = yaml.load(file.read())

    PoloniexDataManager(
        key, config_main[key]['START_DATE'], config_main[key]['PERIOD'])
