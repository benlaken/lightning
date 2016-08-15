import os
import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta
import folium
import getpass
import urllib.request
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


def get_data(start, end, dl_link, username=None, password=None):
    """**Download data from Blitzorg**

    Using a specified time stamp for start and end, data is downloaded at a
    default frequency (10 minute intervals). If a directory called data is not
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
    if not username:
        username = input("Username to access Blitzorg with:")
        password = getpass.getpass(
            prompt='Enter password for {0}:'.format(username))
    auth_handler = urllib.request.HTTPBasicAuthHandler()
    auth_handler.add_password(realm='Blitzortung',
                              uri='http://data.blitzortung.org',
                              user=username,
                              passwd=password)
    opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(opener)
    time_range = pd.date_range(start, end, freq='10min')
    for time_stamp in tqdm(time_range):
        tmp_link = dl_link+'/'.join(return_time_elements(time_stamp))+'.json.gz'
        tmp_name = "./data/bz-"+'-'.join(return_time_elements(time_stamp))+".json.gz"
        if os.path.isfile(tmp_name):
            print("{} exists. Aborting download attempt".format(tmp_name))
        else:
            # print('Downloading: ' + tmp_name) # print name if all okay...
            try:
                    urllib.request.urlretrieve(tmp_link, tmp_name)
            except Exception as inst:
                    print(inst)
                    print('  Encountered unknown error. Continuing.')


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


def count_lightnings(datain, time_step):
    """**Count lightnings in defined time_step**

    Generate time intervals according to the time_step defined and count lightning strikes 
    in these intervals. Statistics is also calculated for lightning detection error and 
    number of stations and added to output dataframe. Time stamps in output data 
    frame correspond to center of time periods in which lightnings are counted. 

    :paramter datain: dataframe (lightning data)
    :parameter time_step: integer (time step in minutes) 

    :Example:
	
	>>> count_lightnings(LN_data, time_step)
     """
    # check if time_step is multiple of 1 day
    if(1440%time_step==0):
        i=0
        # run for loop for all time steps in one day
        for time_interval in gen_time_intervals(extract_date(datain['datetime'][0]), 
                                            (extract_date(datain['datetime'][0])+timedelta(days=1)), 
                                            timedelta(minutes=time_step)):
            # select data in given time_interval
            tmp_LN_data=datain.loc[(datain['datetime']>=time_interval) & 
                        (datain['datetime']<time_interval+timedelta(minutes=time_step))]
            # calculate stats
            stats_err=gen_stats(tmp_LN_data['err'])
            stats_sta=gen_stats(tmp_LN_data['#sta'])
            # format data
            data_list = {'count' : stats_err['count'], 'err_mean' : stats_err['mean'], 'err_std' : stats_err['std'], 
             'err_min' : stats_err['min'], 'err_max' : stats_err['max'], '#sta_mean' : stats_sta['mean'],
             '#sta_std' : stats_sta['std'], '#sta_min' : stats_sta['min'], '#sta_max' : stats_sta['max']}
            # create index
            df_index=time_interval+timedelta(minutes=(time_step/2))
            # create Dataframe
            temp_LN_count=pd.DataFrame(data_list, index=[df_index], columns=['count', 'err_mean', 'err_std', 
                                                                             'err_min', 'err_max', '#sta_mean',
                                                                             '#sta_std', '#sta_min','#sta_max'])
            # add data to existing df
            if(i>=1):
                LN_count=LN_count.append(temp_LN_count)
            else:
                LN_count=temp_LN_count
            i=i+1
        return LN_count
    else:
        print("Variable time_step {0} should have multiple of 1 day (1400 min).".format(time_step))


def gen_stats(datain):
    """**Calculate lightning statitics and return a dictionary**

    Using a raw data in certain time interval calculate mean, std, min, max value for detection 
    error or number of stations.  
    
    :paramter datain: vector with detection error or number of stations
    
    :Example:

    >>> gen_stats(lighning_data['#sta'])
    """
    tmp_dic={}
    tmp_dic['count'] = len(datain)
    tmp_dic['mean'] = np.mean(datain)
    tmp_dic['std'] = np.std(datain)
    tmp_dic['min'] = min(datain)
    tmp_dic['max'] = max(datain)
    return tmp_dic


def gen_time_intervals(start, end, delta):
    """Create time intervals with timedelta periods using datetime for start and end"""
    curr = start
    while curr < end:
        yield curr
        curr += delta


def extract_date(value):
    """Convert timestamp to datetime and set everything to zero except a date"""
    dtime=value.to_datetime()
    dtime=(dtime - timedelta(hours=dtime.hour) - timedelta(minutes=dtime.minute) - 
            timedelta(seconds=dtime.second) - timedelta(microseconds=dtime.microsecond))
    return dtime


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
