import os
import sys
import pkg_resources as pkg
import pandas as pd
from stormstats.storm import read_WWLN, get_map, get_data


def test_examine_date_structure():
    """Check datetime is right type and elements of the datetime are ints"""
    f = pkg.resource_filename('stormstats', "egdata/testdata.loc")
    test_data = read_WWLN(f)
    assert isinstance(test_data['datetime'][0], pd.tslib.Timestamp)
    assert isinstance(test_data['datetime'][0].date().year, int)
    assert isinstance(test_data['datetime'][0].time().microsecond, int)


def test_create_map():
    """Check a map file gets created"""
    f = pkg.resource_filename('stormstats', "egdata/testdata.loc")
    test_data = read_WWLN(f)
    dstr = str(test_data.datetime[0].date())
    filename = 'map_{0}.html'.format(dstr)
    if os.path.isfile(filename):
        os.remove(filename)
    mx = get_map(strike_data=test_data)
    assert os.path.isfile(filename), "Error, no html mapfile found"
    os.remove(filename)


def test_get_data():
    """Check the get_data() function is operating as expected

    Automatically download data from blitzorg using the Urlib module version.
    Requires environment variables to be set so that interactive passwords are
    not needed.
    """
    get_data(start="2015-02-01T06:30", end="2015-02-01T10:05",
             dl_link="http://data.blitzortung.org/Data_1/Protected/Strokes/",
             username=os.environ["Blitzorg_username"],
             password=os.environ["Blitzorg_password"])
    files = os.listdir('tmp_data/')
    if '.DS_Store' in files:
        files.remove('.DS_Store')
    assert len(files) > 21, 'Error, there should be 22 files downloaded'
    assert sorted(files)[0] == "bz-2015-02-01-06-30.json.gz"
    for file in os.listdir('tmp_data'):
        os.remove('tmp_data/'+file)
    os.rmdir('tmp_data')
