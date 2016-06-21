[![Stories in Ready](https://badge.waffle.io/jcalogovic/lightning.svg?label=ready&title=Ready)](http://waffle.io/jcalogovic/lightning)

# Lightning Research

### Dev notes ###

This iPython notebook extracts lightning data from raw WWLN data files and uses
a custom Python module (stormstats) to investigate the data.

Code by: Dr. Jasa Calogovic (Faculty of Geodesy, University of Zagreb) and Dr. Benjamin A. Laken (UCL).
Email: jcalogovic@geof.hr

Open Source (MIT license) analysis of lightning data from <source> using Python.

Testing using py.test.

Auto-documentation via Sphinx.

Issue tracking via waffle.io.

Automated building via Travis CI.

Includes Docker instance for launching the IPython Notebook.

PyPI page: [https://pypi.python.org/pypi/stormstats](https://pypi.python.org/pypi/stormstats)

Run tests via the command `py.test`

## Install ##
During development install the package by running
`git clone <repo>`

`cd <repo path>`

`pip install -e .` # to install the stormstats package in developer mode
