import os
import sys
import pkg_resources as pkg
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import stormstats


def test_examine_date_structure():
    """Check datetime is right type and elements of the datetime are ints"""
    f = pkg.resource_filename('stormstats', "egdata/testdata.loc")
    test_data = stormstats.misc.read_wwln(f)
    assert isinstance(test_data['datetime'][0], pd.tslib.Timestamp)
    assert isinstance(test_data['datetime'][0].date().year, int)
    assert isinstance(test_data['datetime'][0].time().microsecond, int)


def test_create_map():
    """Check a map file gets created"""
    S = stormstats.Storm()
    filename = 'map_2016-11-03.html'
    if os.path.isfile(filename):
        os.remove(filename)
    mx = S.get_map()
    assert os.path.isfile(filename), "Error, no html mapfile found"
    os.remove(filename)


def test_read_blitzorg_csv():
    """Check a geopandas dataframe gets created and filled with data from the
    csv files downloaded via blitzorg.
    """
    S = stormstats.storm.Storm()
    er1 = 'Geopandas object not created'
    er2 = 'Geometry elements are not Shapley point objects'
    er3 = "Error, test data not in geopandas df object"
    assert type(S.df) == gpd.geodataframe.GeoDataFrame, er1
    assert type(S.df['geometry'][0]) == Point, er2
    assert len(S.df) == 100, er3


def test_bzorg_to_geopandas():
    """Check a geopandas dataframe gets created and filled with data"""
    f = pkg.resource_filename('stormstats', "egdata/testdata.loc")
    df = stormstats.misc.wwln_to_geopandas(f)
    er1 = 'Geopandas object not created'
    er2 = 'Geometry elements are not Shapley point objects'
    er3 = "Error, test data not in geopandas df object"
    assert type(df) == gpd.geodataframe.GeoDataFrame, er1
    assert type(df['geometry'][0]) == Point, er2
    assert len(df) == 10, er3


def test_get_data():
    """Check the get_data() function is operating as expected

    Automatically download data from blitzorg using the Urlib module version.
    Requires environment variables to be set so that interactive passwords are
    not needed.
    """
    stormstats.downloader.get_data(start="2015-02-01T06:30",
                                   end="2015-02-01T10:05",
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
