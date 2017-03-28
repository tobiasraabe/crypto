#!/usr/bin/env python3

"""This module provides an Abstract Base Class for prediction models. Every
defined prediction model class has to inherit from this class to be certain
that all necessary functions are defined and the model fits into the existing
code.

The structure of the class is derived from scikit-learn's structure of
estimators. The advantage of that design is that the estimator can be used like
a scikit-learn estimator (e.g. in a pipeline).


Note
----
Abstract Base Classes are used to enforce rigour in programs which provide
a lot of expandability. Mainly, they ensure that all abstract methods are
implemented on instantiation or raise an TypeError otherwise.
See https://dbader.org/blog/abstract-base-classes-in-python and
https://docs.python.org/3/library/abc.html for more information.

"""

from abc import ABC
from abc import abstractmethod


class BasePredictionModel(ABC):

    @abstractmethod
    def __init__(self):
        """The init method creates placeholders for all necessary variables on
        instantiation.

        """
        pass

    @abstractmethod
    def fit(self, y, X, argument):
        """The fit method collects all possible arguments and fits the model to
        the data.

        Arguments
        ---------
        y : array
            An array containing the target values
        X : matrix
            A matrix representation of features
        argument : int, str, ...
            An argument specifying the kind of model fit

        """
        pass

    @abstractmethod
    def predict(self, X):
        """The predict method returns predictions based on the fitted model for
        the new inputs.

        Returns
        -------
        y : array
            An array containing target values for new inputs

        """
        pass
