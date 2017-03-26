#!/usr/bin/env python3

"""This module provides an Abstract Base Class for prediction models. Every
defined prediction model class has to inherit from this class to be certain
that all necessary functions are defined and the model fits into the existing
code.

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
    def predict(self):
        pass

    @abstractmethod
    def cross_validation(self):
        pass
