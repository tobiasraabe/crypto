****************************
From Features to Predictions
****************************

This part explains the design of the project's code regarding feature
generation or selection over prediction models to metrics which evaluate our
methods. We will make use of the amazing *scikit-learn* python library which
provides a powerful framework for using machine learning methods.

In *scikit-learn* there are data, transformers and estimators. Transformers
will modify the representation of the data such that is more suitable for
given estimator. Common procedures are extracting, scaling and selecting
features. Estimators can be used as transformers (Random Forest for feature
selection), but are normally used to make final predictions. At last, there
metrics which can be used to evaluate our prediction model. All of these steps
can be combined in a single Pipeline which will combine all steps from data to
predictions.

This guide uses our moving average implementation as an example of how to embed
your custom models into the *scikit-learn* framework.


Transformers
------------

The first unit of pipelines are transformers which can perform the steps of
feature extraction, preprocessing and selection. As an example, here is our
implementation of a moving averages generator:

.. autoclass:: src.transformers.financial_indicators.MovingAverages
    :members:


Prediction Models
-----------------

.. automodule:: src.prediction_models.moving_average
    :members:


Metrics
-------

.. automodule:: src.metrics.scorer
    :members:


Pipelines
---------

All the above *scikit-learn* objects can be combined into a pipeline which will
automate the process from feature extraction to prediction.

Currently, we have no implementation, but you can see a useful guide an
implementation `here`_.

.. _here: http://zacstewart.com/2014/08/05/pipelines-of-featureunions-of-pipelines.html
