#!/usr/bin/env python3

"""This module provides an Abstract Base Class for feature generation and
processing. Every defined prediction model class has to inherit from this class
to be certain that all necessary functions are defined and the model fits into
the existing code.

The structure of the class is derived from scikit-learn's structure of
preprocessors. The advantage of that design is that the preprocessor can be
used like a scikit-learn preprocessor (e.g. in a pipeline).


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


class BaseFeatureGenerator(ABC):

    @abstractmethod
    def __init__(self):
        """The init method creates placeholders for all necessary variables on
        instantiation.

        """
        pass

    @abstractmethod
    def fit(self, X, argument):
        """The fit method collects all possible arguments and prepares the data
        for the transformation.

        Arguments
        ---------
        X : matrix
            An object which is prepared for transformation
        argument : int, str, ...
            An argument specifying the kind of transformation

        """
        pass

    @abstractmethod
    def transform(self):
        """The transform method returns an transformed object.

        Returns
        -------
        X : matrix
            Transformed input object

        """
        pass

    @abstractmethod
    def fit_transform(self):
        """The fit_transform method combines the calls of fit and transform.

        """
        pass
