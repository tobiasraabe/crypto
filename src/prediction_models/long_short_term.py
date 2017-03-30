#!/usr/bin/env python3

'''
Predicting changes in buying prices using a 4 level LSTM Neural Network

'''

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import pandas as pd
import numpy
from sklearn.base import BaseEstimator


def Lstm(BaseEstimator):

    def __init__(self):

        self.layers = None
        self.trans_type = None
        self.lags = None
        self.reduce = None
        self.iterations = None

    def transform(self,df,layers,trans_type,lags,reduce):

        """Transforming data to fit estimator"""

        if "BTC_POT_TYPE" in df:
            df = df.query("BTC_POT_TYPE == " + trans_type)

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

            # Rescale dataset for gradient descent
            scaler = MinMaxScaler(feature_range=(-1,1))
            ds = scaler.fit_transform(df)

            # reshape input to be [samples, time steps, features]
            ds = numpy.reshape(ds, (ds.shape[0], 1, ds.shape[1]))

        else:
            return "Input is not a BTC_POT dataframe."

        return ds, dfOut

    def fit(self,df,layers: int = 4,trans_type: str = "buy",
            lags: int = 3,reduce: int = 1000, iterations: int = 10):

        """Model fitting"""
        ds, dfOut = self.transform(df,layers,trans_type,lags,reduce)

        self.dfOut = dfOut

        # sequential model
        modelR = Sequential()
        # type of model, layer and input declaration
        modelR.add(LSTM(layers, input_shape=(None,len(ds))))
        modelR.add(Dense(1))
        modelR.compile(loss='mean_squared_error', optimizer='adam')
        # model fit
        self.model = modelR.fit(ds, dfOut, epochs=iterations, batch_size=1, verbose=2)

        return self

    def predict(self,x):
        """Prediction method. returns array of predictionf change"""

        # predict based on model
        return self.dfOut, self.model.predict(ds)
