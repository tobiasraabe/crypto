.. _testing:


*******
Testing
*******

This project comes with some testing utilities to ensure that the project is
working correctly.


pytest
------

Our testing suite for Python code is `pytest`_ which provides a very flexible,
intuitive approach of writing tests.

.. _pytest: https://docs.pytest.org/en/latest/

During the build phase of Waf, all tests are completed before advancing to
the next step. If an error is raised, Waf interrupts the build and the error
has to be resolved.


tox
---

The project also provides support for `Tox`_ which is a virtualenv manager and
a wrapper for all of your desired tests. There are a number of test options
available for this project. Tox is especially useful since it provides an easy
command to run the pytest tests inside the project without using Wafs build
process.

.. _Tox: https://tox.readthedocs.io/en/latest/

You can run the whole suite of tests by typ::

    $ tox

You can test separately by typing::

    $ tox -e ${TOXENV}

The tests for the python code of the project is available by typing
(e.g. Python 3.5)::

    $ tox -e py35

If you want to lint code and documentation, type::

    $ tox -e linters

or if you want to do that separately::

    $ tox -e flake8
    $ tox -e doc8
