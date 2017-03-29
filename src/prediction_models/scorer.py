#!/usr/bin/env python3

"""This module contains the scoring function which will be used to evaluate
an prediction model.

We will start with a simple idea and neglect a number of other issues (e.g.
fees per trade, moving the market with trades).

The simplest idea is to convert predictions to tertiary statements where a
higher predicted price in the next period translates to a buy decision, a
lower price to a sell decision, and a no change to a halt decision.

The following notation is used: :math:`\mu(x)` is an indicator function,
:math:`t` represents the current period, :math:`t+1` the future period, and
:math:`p_t` the price in period :math:`t`.

.. math::

    \mu(p_t) =  \begin{cases}
                    1 & \text{if } p_{t+1} >  p_t\\
                    0 & \text{if } p_{t+1} <= p_t
                \end{cases}

After transforming the series with the former indicator function, the resulting
series holds the so called regimes which means it is indicating periods with
rising prices and constant or falling prices.

Next, we want to obtain a series of signals indicating whether we change our
current position. A signal is calculated like this:

.. math::

    Signal(p_t) =   \begin{cases}
                         1 & \text{if } \mu(p_t) - \mu(p_{t-1}) = 1 - 0\\
                         0 & \text{if } \mu(p_t) - \mu(p_{t-1}) = 1 - 1 =
                             0 - 0\\
                        -1 & \text{if } \mu(p_t) - \mu(p_{t-1}) = 0 - 1

Suppose we get signals ``1`` in time period ``t`` and ``-1`` in ``t+s``, then
we can calculate returns of this trade with this formula:

.. math::

    Returns(p_t, p_{t+s}) = \\frac{p_{t+s} - p_{t}}{p_{t+s}}

In the end, the scorer sums up all returns of each trade and reports the
number.

Todo
----
- Implement fees from Poloniex into the evaluation algorithm
- Implement an adjustment that one has the power to move the market and prices
  will change because of your trade

"""

import numpy as np
from sklearn.metrics.scorer import make_scorer


def moving_average_score(truth, prediction):
    """This scorer calculates the percentage of returns for the calculated
    signals.

    Returns
    -------
    cum_returns : float
        Float indicating the sum of returns for trades by signals

    Todo
    ----
    - Implement as sklearn scorer, but this is only working if MovingAverage
      becomes an sklearn estimator. Hell yeah...

    """
    # Focus on trades (np.array([BTC_POT_CLOSE, SIGNALS]))
    trades = np.array([
        truth[(prediction == -1) | (prediction == 1)],
        prediction[(prediction == -1) | (prediction == 1)]
    ])
    # Calculates returns
    returns = (trades[0] - np.roll(trades[0], 1)) / trades[0]
    # Use only returns on sells and calculate sum
    cum_returns = sum(returns[trades[1] == -1])

    return cum_returns


def portfolio_score(truth, prediction):
    """This scorer calculates the percentage of returns for the calculated
    signals.

    Returns
    -------
    cum_returns : float
        Float indicating the sum of returns for trades by signals

    Todo
    ----
    - Implement as sklearn scorer, but this is only working if MovingAverage
      becomes an sklearn estimator. Hell yeah...

    """
    # Vectorized if-else condition to calculate bullish or bearish periods
    regimes = np.where(prediction - truth > 0, 1, 0)
    # Vector containing signals to buy, halt, sell (1, 0, -1)
    signals = regimes - np.roll(regimes, 1)
    # np.roll places the last values at the beginning which has no meaning
    # in this case. It would be better to cast the values to np.NaN, but
    # that is not allowed in integer arrays. Therefore, we will use -2.
    signals[0] = -2
    # Focus on trades (np.array([BTC_POT_CLOSE, SIGNALS]))
    trades = np.array([
        truth[(signals == -1) | (signals == 1)],
        signals[(signals == -1) | (signals == 1)]
    ])
    # Calculates returns
    returns = (trades[0] - np.roll(trades[0], 1)) / trades[0]
    # Use only returns on sells and calculate sum
    cum_returns = sum(returns[trades[1] == -1])

    return cum_returns


portfolio_scorer = make_scorer(portfolio_score, greater_is_better=True)
