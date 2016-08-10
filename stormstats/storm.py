import os
import numpy as np
import pandas as pd
import datetime as dt
import folium
import getpass
import requests
import gzip
from tqdm import tqdm


class Storm(object):
    """Main analysis class"""
    def __init__(self):
        pass

    def read_data(self):
        """Class for reading data"""
        pass

    def foo(self):
        """Class for foo"""
        pass


def get_data(start, end, dl_link, freq='10min'):
    """**Download data from Blitzorg**

    Using a specified time stamp for start and end, data is downloaded at a
    default frequency of 10 minute intervals. If a directory called data is not
    present, it will be added to the cwd as the target for the downloads.

    :paramter start: string
    :parameter end: string
    :parameter freq: string
    :paramater dl_link: string

    :Example:

    >>> get_data(start="2015-02-01T06:30", end="2015-02-01T10:05",
                dl_link="http://data.blitzortung.org/Data_1/Protected/Strokes/")
    """
    path = './data'
    try:
        os.stat(path)
    except:
        os.mkdir(path)
    username = input("Username to access Blitzorg with:")
    password = getpass.getpass(prompt='{0} Bzorg passwd'.format(username))
    time_range = pd.date_range(start, end, freq=freq)
    for time_stamp in tqdm(time_range):
        tmp_link = dl_link+'/'.join(return_time_elements(time_stamp))+'.json.gz'
        tmp_name = "./data/bz-"+'-'.join(return_time_elements(time_stamp))+".json.gz"
        if os.path.isfile(tmp_name):
            print("{} exists. Aborting download attempt".format(tmp_name))
        else:
            r = requests.get(tmp_link, auth=(username, password))
            if r.status_code == 200:
                # Save the binary content
                f = open(tmp_name, 'wb')
                for chunk in r.iter_content(chunk_size=512 * 1024):
                    if chunk:
                        f.write(chunk)
                    f.close()
                    # Read and simultaneouslyuUncompress the data into JSON
                    inF = gzip.open(tmp_name, 'rb')
                    s = inF.read()
                    inF.close()
                    fname = tmp_name[:-3]
                    uncompressed_path = os.path.join(fname)
                    open(uncompressed_path, 'wb').write(s)
                    # Remove first binary file
                    os.remove(tmp_name)
            else:
                raise ValueError("{0} HTTP status".format(r.status_code))


def return_time_elements(time_stamp):
    """Returns formatted strings of time stamps for HTML requests.

    :parameters time_range: pandas.tslib.Timestamp
    """
    yyyy = str(time_stamp.year)
    mm = "%02d" % (time_stamp.month,)
    dd = "%02d" % (time_stamp.day,)
    hr = "%02d" % (time_stamp.hour,)
    mins = "%02d" % (time_stamp.minute,)
    return yyyy, mm, dd, hr, mins


def add_to_map(map_obj, lat, lon, date_time, key, cluster_obj):
    """Add individual elements to a foilum map using a cluster object"""
    text = "Event {0} at {1}".format(key, str(date_time.time()))
    folium.Marker([lat, lon], popup=text).add_to(cluster_obj)


def get_map(strike_data, create_html=True):
    """Strike data should be a pd.DF from the WWLN
    data files read by read_WWLN()"""
    num_rows = len(strike_data)
    if num_rows > 1000:
        print("Warning, you have requested a large amount of data be mapped")
        print("I am limiting your request to the first 1,000 rows, as this")
        print("is currently only a preview feature.")
        strike_data = strike_data[0:1000]
    m = folium.Map(location=[0.0, 0.01], zoom_start=2)
    marker_cluster = folium.MarkerCluster().add_to(m)

    for event in strike_data.index:
        add_to_map(map_obj=m, date_time=strike_data.datetime[event],
                   cluster_obj=marker_cluster, lat=strike_data.lat[event],
                   lon=strike_data.lon[event], key=event)
    if create_html:
        data_date = str(strike_data.datetime[0].date())
        m.save('map_{0}.html'.format(str(strike_data.datetime[0].date())))
    return m


def read_WWLN(file):
    """Read WWLN file"""
    tmp = pd.read_csv(file, parse_dates=True, header=None,
                      names=['date', 'time', 'lat', 'lon', 'err', '#sta'])
    # Generate a list of datetime objects with time to miliseconds
    list_dts = []
    for dvals, tvals, in zip(tmp['date'], tmp['time']):
        list_dts.append(gen_datetime(dvals, tvals))
    dtdf = pd.DataFrame(list_dts, columns=['datetime'])
    result = pd.concat([dtdf, tmp], axis=1)
    result = result.drop(['date', 'time'], axis=1)
    return result


def gen_datetime(dvals, tvals):
    dvals = [int(t) for t in dvals.split('/')]
    year, month, day = dvals
    hh, mm, sec_micro = tvals.split(':')
    hh = int(hh)
    mm = int(mm)
    ss, mss = sec_micro.split('.')
    ss = int(ss)
    mss = int(mss)
    return dt.datetime(year, month, day, hh, mm, ss, mss)


if __name__ == "__main__":
    print("Executing lightning_analysis.py directly")
