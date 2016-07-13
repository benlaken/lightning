import os
import sys
import pandas as pd
from ..storm import read_WWLN, get_map


def test_examine_date_structure():
    """Check datetime is right type and elements of the datetime are ints"""
    test_data = read_WWLN("stormstats/egdata/testdata.loc")
    assert isinstance(test_data['datetime'][0], pd.tslib.Timestamp)
    assert isinstance(test_data['datetime'][0].date().year, int)
    assert isinstance(test_data['datetime'][0].time().microsecond, int)


def test_map_created():
    """Check a map file gets created"""
    test_data = read_WWLN("stormstats/egdata/testdata.loc")
    dstr = str(test_data.datetime[0].date())
    filename = 'map_{0}.html'.format(dstr)
    if os.path.isfile(filename):
        # check if the file already exists and remove it if it does
        os.remove(filename)
    # run the map function, and create a new .html map
    mx = get_map(strike_data=test_data)
    assert os.path.isfile(filename), "Error, no html mapfile found"
