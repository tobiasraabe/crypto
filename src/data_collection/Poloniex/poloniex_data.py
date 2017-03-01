#!/usr/bin/env python
import datetime
import os
import pandas as pd
import poloniex
import sys
import requests
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

    def __init__(self, key):
        self.key = key
        self.path_config_main = ppj(
            'IN_DATA_COLLECTION', 'Poloniex', 'poloniex_config.yml')
        self.path_config_temp = ppj('OUT_DATA_RAW', self.key + '.yml')

        self.start = None
        self.period = None
        self.multiplicator = 1.1

        self.generate_trade_history()
        self.generate_chart_data()

    def generate_trade_history(self):
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
        finally:
            print('START: Generating data for {} - Trade History.'
                  .format(self.key))
            while True:
                self.period = self.validate_period(
                    multiplicator=self.multiplicator)
                self.gen_th()
                self.start += self.period
                if self.start == END_DATE:
                    break

            self.remove_duplicates('trade_history')

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
            print('SUCCESS: Created {}-trade_history'.format(self.key))

    def generate_chart_data(self):
        try:
            with open(self.path_config_temp) as file:
                config_temp = yaml.load(file.read())
                self.start = config_temp['chart_data']['END_DATE']
        except (FileNotFoundError, KeyError):
            with open(self.path_config_main) as file:
                config_main = yaml.load(file.read())
            self.start = config_main[self.key]['START_DATE']
        finally:
            print('START: Generating data for {} - Chart Data'
                  .format(self.key))
            self.gen_cd()
            self.remove_duplicates('chart_data')

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

            print('SUCCESS: Created {}-chart_data'.format(self.key))

    def validate_period(self, multiplicator=1) -> int:
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

        self.period = int(self.period * multiplicator)

        polo = poloniex.Poloniex()

        # Hotfix for somehow malformed intervals which return a ReadTimeout
        # never happened before but now. There must be a difference in code to
        # the previous commit or it is just bad luck. However, reducing the
        # interval solves this issue.
        while True:
            try:
                api_out = polo.marketTradeHist(
                    self.key, start=self.start, end=self.start + self.period)
            except requests.exceptions.ReadTimeout:
                self.period = int(self.period * 0.9)
                print('WARNING: HOTFIX REDUCED INTERVAL')
            else:
                break

        print('Pair: {}, Start: {}, Period: {}, End: {}, Left: {},'
              ' No. items: {}'
              .format(self.key, self.start, self.period,
                      self.start + self.period,
                      END_DATE - self.start - self.period, len(api_out)))

        time.sleep(DELAY)

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
        """Recieves a valid API call and writes ``DataFrame`` to disk.

        Parameters
        ----------
        pair : str
            Exchange key

        """
        polo = poloniex.Poloniex()
        path_data = ppj(
            'OUT_DATA_RAW', self.key + '_trade_history.csv')

        df = pd.DataFrame(polo.marketTradeHist(
            self.key,
            start=self.start,
            end=self.start + self.period)
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
        polo = poloniex.Poloniex()
        path_data = ppj('OUT_DATA_RAW', self.key + '_chart_data.csv')

        # Hotfix for somehow malformed intervals which return a ReadTimeout
        # never happened before but now. There must be a difference in code to
        # the previous commit or it is just bad luck. However, reducing the
        # interval or trying again solves this issue.
        while True:
            try:
                api_out = polo.returnChartData(
                    self.key, period=300, start=self.start, end=END_DATE)
            except requests.exceptions.ReadTimeout:
                print('WARNING: HOTFIX CATCHED ERROR. CONTINUE')
                continue
            else:
                break

        df = pd.DataFrame(api_out)

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
        df.sort_values(subset, axis=0, inplace=True)

        path_data = ppj(
            'OUT_DATA_RAW', self.key + '_' + method_name + '.csv')
        df.to_csv(path_data)


if __name__ == '__main__':
    key = sys.argv[1]

    PoloniexDataManager(key)
