import os
import sys
import pandas as pd
from ..storm import Storm, read_WWLN


def test_reading_function():
    """Example of how to run a test. In this case to see if reading
    is a function. """
    def foo(): pass
    assert type(Storm.read_data) == type(foo)


def test_examine_date_structure():
    test_data = read_WWLN("egdata/testdata.loc")
    """Check datetime is right type and elements of the datetime are ints"""
    assert isinstance(test_data['datetime'][0], pd.tslib.Timestamp)
    assert isinstance(test_data['datetime'][0].date().year, int)
    assert isinstance(test_data['datetime'][0].time().microsecond, int)
