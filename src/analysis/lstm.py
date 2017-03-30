#!/usr/bin/env python3

"""This module outputs return values for different moving averages.

"""

import matplotlib.pyplot as plt
import seaborn
import sys

from bld.project_paths import project_paths_join as ppj
from sklearn.externals import joblib
from src.prediction_models.long_short_term import Lstm
from src.prediction_models.scorer import portfolio_score
from src.prediction_models.scorer import roc_score
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy



if __name__ == '__main__':
    key = sys.argv[1]
    layers = int(sys.argv[2])
    lags = int(sys.argv[3])
    reduce = int(sys.argv[4])
    iterations = int(sys.argv[5])

    # load dataset
    df = joblib.load(
        ppj('OUT_DATA_PROCESSED','{}_trade_history.p.lzma'.format(key)))

    # reduce dataframe to only 'buy' transactions as those drive the price
    df = df.query('BTC_POT_TYPE == "buy"')

    # create time difference between 2 transactions
    df['tvalue'] = df.index
    df['deltat'] = df['tvalue'] - df['tvalue'].shift(1)

    # create lags for BTC price sold/purchased at
    for i in range(1,lags+1):
        df['BTC_POT_RATE_'+str(i)] = df["BTC_POT_RATE"].shift(i)

    # create lags for total BTC value sold/purchased
    for i in range(1,lags+1):
        df['BTC_POT_TOTAL_'+str(i)] = df["BTC_POT_TOTAL"].shift(i)

    # remove unused vars from df
    df = df.drop(['tvalue','BTC_POT_AMOUNT','BTC_POT_TYPE'],1)

    # create pot rate difference for dependent variable
    df['ratechange'] = df['BTC_POT_RATE'] - df['BTC_POT_RATE'].shift(1)

    # drop all rows containing NaNs
    df = df.dropna(axis=0,how="any")

    # allow for dataset reduction because of time constraints
    if reduce is not None:
        df = df.iloc[0:reduce,:]

        # move outcome var to separate df
    dfOut = df.iloc[:,-1]
    # remove first 3 vars RATE TOTAL deltat because not useful
    df = df.iloc[:,3:-1]

    # applying scaler to dataframe to improve gradient descent
    # output is numpy array
    scaler = MinMaxScaler(feature_range=(-1,1))
    ds = scaler.fit_transform(df)

    # reshape input to be [samples, time steps, features]
    ds = numpy.reshape(ds, (ds.shape[0], 1, ds.shape[1]))


    # assigning fitting function
    longstm = Lstm()
    lstmfit = longstm.fit(df=ds,Y=dfOut,layers=layers,lags=lags,
                              reduce=reduce, iterations=iterations)

    # predict results from LSTM
    lstmresults = lstmfit.predict(ds)

    # feeding into portfolio_score
    #portfolio_score(dfOut.as_matrix().shape, lstmresults)

    # plotting creator operator characteristic for up and down changes in
    # 'buy' transactions

    posfpr, postpr, posroc_auc, negfpr, negtpr, negroc_auc = roc_score(dfOut.as_matrix(),lstmresults)

    plt.title('Receiver Operating Characteristic')
    plt.plot(posfpr, postpr, 'b', label = '"up" AUC = %0.2f' % posroc_auc)
    plt.plot(negfpr, negtpr, 'b', label = '"down" AUC = %0.2f' % negroc_auc)
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()

