[![Build Status](https://travis-ci.org/AWehrhahn/PyReduce.svg?branch=master)](https://travis-ci.org/AWehrhahn/PyReduce)
[![Documentation Status](https://readthedocs.org/projects/pyreduce-astro/badge/?version=latest)](https://pyreduce-astro.readthedocs.io/en/latest/?badge=latest)
[![Updates](https://pyup.io/repos/github/AWehrhahn/PyReduce/shield.svg)](https://pyup.io/repos/github/AWehrhahn/PyReduce/)

# PyREDUCE

PyReduce is a port of the [REDUCE](http://www.astro.uu.se/~piskunov/RESEARCH/REDUCE/) package to Python3.
It is a complete data reduction pipeline for the echelle spectrographs, e.g. HARPS or UVES.

Detailed documentation is available at [ReadTheDocs](https://pyreduce-astro.readthedocs.io/en/latest/index.html).

Installation
------------
PyReduce can be installed using pip using the following command: ``pip install pyreduce-astro``

PyReduce uses CFFI to link to the C code, on non-linux platforms you might have to install libffi.
See also https://cffi.readthedocs.io/en/latest/installation.html#platform-specific-instructions for details.

How To
------
PyReduce is designed to be easy to use, but still be flexible.
``examples/uves_example.py`` is a good starting point, to understand how it works.
First we define the instrument, target, night, and instrument mode (if applicable) of our reduction. Then we tell PyReduce where to find the data, and lastly we define all the specific settings of the reduction (e.g. polynomial degrees of various fits) in a json configuration file.
We also define which steps of the reduction to perform. Steps that are not specified, but are still required, will be loaded from previous runs if possible, or executed otherwise.
All of this is then passed to pyreduce.reduce.main to start the reduction.

In this example, PyReduce will plot all intermediary results, and also plot the progres during some of the steps. Close them to continue calculations, if it seems nothing is happening. Once you are statisified with the results you can disable them in settings_UVES.json (with "plot":false in each step) to speed up the computation.

Papers
------
The original REDUCE paper: [doi:10.1051/0004-6361:20020175](https://doi.org/10.1051/0004-6361:20020175)

A paper describing the changes and updates of PyReduce is in preperation.
