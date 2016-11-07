import os
import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta
import folium
from shapely.geometry import Point
import geopandas as gpd
import pkg_resources as pkg


class Storm(object):
    """Main analysis class. Optional kwargs, f can set file path and name
    of csv file downloaded from Blitzorg to load.
    """
    def __init__(self, **kwargs):
        self.df = self.read_blitzorg_csv(kwargs.get('f'))

    def get_map(self, create_html=True):
        """Strike data should be a pd.DF from the WWLN data files read by
        read_WWLN()"""
        strike_data = self.df
        num_rows = len(self.df)
        if num_rows > 1000:
            print("Warning, you have requested lots of data be mapped." /
                  " Limiting your request to the first 1,000 rows" /
                  " as this is currently only a preview feature.")
            strike_data = self.df[0:1000]
        m = folium.Map(location=[0.0, 0.01], zoom_start=2)
        marker_cluster = folium.MarkerCluster().add_to(m)
        for event in strike_data.index:
            self.add_to_map(map_obj=m,
                            date_time=strike_data.dt[event],
                            cluster_obj=marker_cluster,
                            lat=strike_data.geometry[event].y,
                            lon=strike_data.geometry[event].x,
                            key=event)
        if create_html:
            data_date = str(strike_data.datetime.iloc[0].date())
            m.save('map_{0}.html'.format(strike_data.dt[0].split()[0]))
        return m

    @staticmethod
    def read_blitzorg_csv(f=None):
        """
        Function to read csv data downloaded from Blitzorgs historical data
        section. Time is in POSIX timestamps (x1000000000). An eg is kept in
        stormstats/egdata/archive_2_raw.txt. If no data file is specified
        the function will assume you want to read this example data. Geopandas
        dataframe will be returned.

        :paramter f: optional string giving path/filename of csv data

        :Example:

        >>> stormstats.storm.read_blitzorg_csv(f=None)
        """
        factor = 1000000000  # don't change this magic number! Its from Bzorg.
        if f:
            tmp = pd.read_csv(f)
        else:
            f = pkg.resource_filename('stormstats', "egdata/archive_2_raw.txt")
            tmp = pd.read_csv(f)
        dt_list = [dt.datetime.fromtimestamp(ts/factor).strftime(
            '%Y-%m-%d %H:%M:%S:%f') for ts in tmp.time]
        tmp_list = [[Point(lon, lat), ts] for lon, lat, ts in
                    zip(tmp.lon, tmp.lat, dt_list)]
        df = gpd.GeoDataFrame(tmp_list, columns=['geometry', 'dt'])
        return df

    @staticmethod
    def add_to_map(map_obj, lat, lon, date_time, key, cluster_obj):
        """Add individual elements to a foilum map in a cluster object"""
        text = "Event {0} at {1}".format(key, date_time.split()[1])
        folium.Marker([lat, lon], popup=text).add_to(cluster_obj)
