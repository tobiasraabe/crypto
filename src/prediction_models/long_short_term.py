#!/usr/bin/env python3

'''
Predicting changes in buying prices using a 4 level LSTM Neural Network

'''
from sklearn.base import BaseEstimator
from keras.layers import Dense, LSTM
from keras.models import Sequential


class Lstm(BaseEstimator):

    def __init__(self):

        self.layers = None
        self.lags = None
        self.reduce = None
        self.iterations = None

    def fit(self,df,Y,layers: int = 4, lags: int = 3,reduce: int = 1000,
            iterations: int = 10):

        self.dfOut = Y

        # sequential model
        modelR = Sequential()
        # type of model, layer and input declaration
        modelR.add(LSTM(layers, input_shape=(None,lags*2)))
        modelR.add(Dense(1))
        modelR.compile(loss='mean_squared_error', optimizer='adam')
        # model fit
        self.model = modelR.fit(df, Y, epochs=iterations, batch_size=1, verbose=2)

        return self

    def predict(self,x):
        """Prediction method. returns array of predictionf change"""

        # predict based on model
        return self.model.predict(df)
