import os
import sys
import pandas as pd
from ..storm import read_WWLN, get_map, get_data


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


def test_get_data():
    """Check the get_data() function is operating as expected

    Automatically download data from blitzorg using the Urlib module version.
    Requires environment variables to be set so that interactive passwords are
    not needed.
    """
    user = os.environ["Blitzorg_username"]
    passwd = os.environ["Blitzorg_password"]
    get_data(start="2015-02-01T06:30", end="2015-02-01T10:05",
             dl_link="http://data.blitzortung.org/Data_1/Protected/Strokes/",
             username=os.environ["Blitzorg_username"], password=os.environ["Blitzorg_password"])
    files = os.listdir('data/')
    assert len(files) is 22, 'Error, there should be 22 files downloaded'
    assert sorted(files)[0] == "bz-2015-02-01-06-30.json.gz", "First file should be bz-2015-02-01-06-30.json.gz"
    assert sorted(files)[-1] == 'bz-2015-02-01-10-00.json.gz', "Last file should be bz-2015-02-01-10-00.json.gz"
