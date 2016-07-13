import os
import sys
import pandas as pd
from ..storm import Storm, read_WWLN


def test_examine_date_structure():
    """Check datetime is right type and elements of the datetime are ints"""
    test_data = read_WWLN("stormstats/egdata/testdata.loc")
    assert isinstance(test_data['datetime'][0], pd.tslib.Timestamp)
    assert isinstance(test_data['datetime'][0].date().year, int)
    assert isinstance(test_data['datetime'][0].time().microsecond, int)
