.. _introduction:


************
Introduction
************

This is the documentation on the **Cryptocurrency Market Prediction** project.


.. _getting_started:

Getting started
===============

This project concerns the prediction of trading behavior in crypto currencies, i.e. blockchain based digital currencies, on the crypto exchange `Poloniex <http://poloniex.com/>`_. In particular I chose a crypto currency called *PotCoin* as my target of investigation.

Poloniex is a US based online trading platform for digital currencies. Digital currencies emerged shortly after the advent of BitCoin in 2009 :cite:`nakamoto2008bitcoin,cheung2015`. At the time of writing Poloniex offers trading in 70 different crypto currencies from major ones like industry backed Ethereum to obscure ones like BlackCoin.

`Potcoin <http://www.potcoin.com>`_ emerged in 2014 as a community project to start a digital currency for the emerging Marijuana industry in the US. The core the development team forked the original Litecoin wallet application and started out as a Litecoin clone simply changing labels and running separated network but still using *Proof-of-work* as coin mining mechanism. However, by midst 2016 Potcoin moved from Proof-of-work to *Proof-of-stake* as one of the first currencies employing this technology and stating community focus as one of the reasons.
The currency has a market volume of approximately 20 Mio. US Dollars and strives to provide a digital currency infrastructure for legalized Marijuana around the globe (`Official Reddit Potcoin thread <https://www.reddit.com/r/potcoin/>`_).

I chose Potcoin as it offers an interesting premise of a subject but also because the trading volume and speed, even though not negligible, is not too high, allowing for collection of a considerable timespan of data.
This programming project itself uses the public API of Poloniex and Twitter to collect the raw data. It could therefore quickly be adapted to be used for predicting other digital currencies, traded on Poloniex.

