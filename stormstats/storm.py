import os
import numpy as np
import pandas as pd
import datetime as dt
import folium
import getpass


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
    """Example of use:

    get_data(start="2015-02-01T06:30", end="2015-02-01T10:05",
             dl_link="http://data.blitzortung.org/Data_1/Protected/Strokes/")
    """
    username = input("Username to access Blitzorg with:")
    password = getpass.getpass(
        prompt='Blitzorg password for {0}:'.format(username))
    auth_handler = urllib.request.HTTPBasicAuthHandler()
    auth_handler.add_password(realm='Blitzortung',
                              uri='http://data.blitzortung.org',
                              user=username,
                              passwd=password)
    opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(opener)     # install globally (bad idea)
    time_range = pd.date_range(start, end, freq=freq)
    for time_stamp in time_range:
        tm_month = "%02d" % (time_stamp.month,)
        tm_day = "%02d" % (time_stamp.day,)
        tm_hour = "%02d" % (time_stamp.hour,)
        tm_min = "%02d" % (time_stamp.minute,)
        # The below should use os to check if the data/ folder exists
        tmp_link = dl_link+str(time_stamp.year)+"/"+tm_month+"/"+tm_day+"/"+tm_hour+"/"+tm_min+".json.gz"
        tmp_name = "./data/blitz"+str(time_stamp.year)+tm_month+tm_day+"T"+tm_hour+tm_min+".json.gz"
        if not os.path.isfile(tmp_name):
            print('Downloading: ' + tmp_name)
            try:
                    urllib.request.urlretrieve(tmp_link, tmp_name)
            except Exception as inst:
                    print(inst)
                    print('  Encountered unknown error. Continuing.')


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
