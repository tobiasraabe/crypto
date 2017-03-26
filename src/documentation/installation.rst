.. _installation:

************
Installation
************

The project has some dependencies which have to be installed for a successful
run.


Python Environment
==================

For the project to work it is best to use an 3.5.2 or 3.6 Anaconda
distribution. This is definitely not lightweight but we encountered several
problems by creating an environment from file when we wanted to move the
project to other systems. The problem seems to occur with packages which rely
on additional C code (i.e. scikit-learn, lxml).

Next, we will need to install an additional package from Github.

.. code-block:: console

    pip3 install git+https://github.com/s4w3d0ff/python-poloniex.git

To install additional packages, run

.. code-block:: console

    pip3 install -r requirements.txt



Project
=======

You can download the project to your disk by using

.. code-block:: console

    git clone --recursive https://github.com/tobiasraabe/crypto.git

The ``--recursive`` flag is needed to include submodules. If you forgot to do
that, take a look at :ref:git_submodules.


Data files
==========

In advance one also has to download some data files. Since the data collection
from Twitter proved to be very time-consuming, it is preferred to download
the files beforehand. By running

.. code-block:: console

    python3 download_statics

the data is automatically downloaded and copied to your ``crypto/src/static``
folder. Files with an identical name are overwritten.

This step was necessary since git is not supposed to contain large files which
will blow up your repository size. In the case that you accidentally committed
some datasets or something similar there is a tool to clean your repository
afterwards. `BFG Repo-Cleaner`_ will check each commit and then change the ones
carrying your datasets.

.. _BFG Repo-Cleaner: https://rtyley.github.io/bfg-repo-cleaner/


.. git_submodules::

Git submodules
==============

The project relies on submodules which are only downloaded if you add the
recursive flag while cloning the repository. If you forgot to do that or
forked the submodules and made additional changes, there is a pythonic shortcut
to recursively update all of your submodules by running

.. code-block:: console

    python3 update.py

