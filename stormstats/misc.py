import os
import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta
import folium
from shapely.geometry import Point
import geopandas as gpd
import pkg_resources as pkg


def read_wwln(file):
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


def wwln_to_geopandas(file):
    """Read data from Blitzorg first using pandas.read_csv for convienence, and
    then convert lat, lon points to a shaleply geometry POINT type.
    Finally put this gemoetry into a geopandas dataframe and return it."""
    tmp = pd.read_csv(file, parse_dates=True, header=None,
                      names=['date', 'time', 'lat', 'lon', 'err', '#sta'])
    list_dts = [gen_datetime(dvals, tvals)
                for dvals, tvals in zip(tmp['date'], tmp['time'])]
    points = [[Point(tmp.lat[row], tmp.lon[row]), dt]
              for row, dt in zip(tmp.index, list_dts)]
    df = gpd.GeoDataFrame(points, columns=['geometry', 'dt'])
    return df


def gen_listfiles(ext, data_path=current_path, start_date=None, end_date=None):
    """**Generate list of files in data directory**

    Using a specified data path and extension generate list of files in data
    directory. If start_date and end_date aren't specified, all files in the
    data directory are selected.

    :paramter data_path: string
    :parameter ext: string
    :parameter start_date: time string in format mm-dd-yyy (optional)
    :paramater end_date: time string in format mm-dd-yyy (optional)

    :Example:

    >>> gen_listfiles(data_path='./data', ext='.loc', start_date='01-01-2016',
    end_date='01-10-2016')
    """
    # make list of all files in data directory with certain extension ext
    listfiles = [fn for fn in os.listdir(data_path) if (fn.endswith(ext))]
    # check if start_date & end_date are set
    if (start_date is not None) or (end_date is not None):
        all_dates = pd.date_range(start_date, end_date, freq='D')
        # make list with files in selected range
        files = []
        for date in all_dates:
            yyyy = str(date.year)
            mm = "%02d" % (date.month,)
            dd = "%02d" % (date.day,)
            file = 'A'+yyyy+mm+dd+ext
            files.append(file)
        # compare and return matches
        listfiles = set(listfiles).intersection(files)
        return files
    # if start and end dates aren't set use all files in data dir
    else:
        return listfiles


def count_lightning(datain, time_step):
    """**Count lightning strikes detected within a defined time_step**

    Generate time intervals according to the time_step defined and count
    lightning strikes in these intervals. Statistics are also calculated for
    lightning detection errors and the number of stations and added to an
    output dataframe. Time stamps in output dataframe correspond to center of
    time periods in which lightning are counted.

    :paramter datain: dataframe (lightning data)
    :parameter time_step: integer (time step in minutes)

    :Example:

     >>> count_lightning(LN_data, time_step)
     """
    if(1440 % time_step == 0):  # check if time_step is multiple of 1 day
        i = 0
        # run for loop for all time steps in one day
        for time_interval in gen_time_intervals(extract_date(datain['datetime'].iloc[0]),
                                                (extract_date(datain['datetime'].iloc[0])+timedelta(days=1)),
                                                timedelta(minutes=time_step)):
            # select data in given time_interval
            tmp_LN_data = datain.loc[(datain['datetime'] >= time_interval) &
                                     (datain['datetime'] < time_interval +
                                      timedelta(minutes=time_step))]
            # calculate stats
            stats_err = gen_stats(tmp_LN_data['err'])
            stats_sta = gen_stats(tmp_LN_data['#sta'])
            d = {'count': stats_err['count'],
                 'err_mean': stats_err['mean'],
                 'err_std': stats_err['std'],
                 'err_min': stats_err['min'],
                 'err_max': stats_err['max'],
                 '#sta_mean': stats_sta['mean'],
                 '#sta_std': stats_sta['std'],
                 '#sta_min': stats_sta['min'],
                 '#sta_max': stats_sta['max']}
            col_names = [k for k in d.keys()]
            df_index = time_interval+timedelta(minutes=(time_step/2))
            temp_LN_count = pd.DataFrame(d, index=[df_index],
                                         columns=col_names)
            # add data to existing df
            if(i >= 1):
                LN_count = LN_count.append(temp_LN_count)
            else:
                LN_count = temp_LN_count
            i = i + 1
        return LN_count
    else:
        print("time_step {0} multiple of 1 day (1400 min)".format(time_step))


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
    # if there is no lightning strikes set nan values for all stats parameters
    if(tmp_dic['count'] == 0):
        tmp_dic['mean'] = np.nan
        tmp_dic['std'] = np.nan
        tmp_dic['min'] = np.nan
        tmp_dic['max'] = np.nan
    else:
        tmp_dic['mean'] = np.mean(datain)
        tmp_dic['std'] = np.std(datain)
        tmp_dic['min'] = min(datain)
        tmp_dic['max'] = max(datain)
    return tmp_dic


def gen_time_intervals(start, end, delta):
    """Create time intervals with timedelta periods using datetime for start
    and end
    """
    curr = start
    while curr < end:
        yield curr
        curr += delta


def extract_date(value):
    """
    Convert timestamp to datetime and set everything to zero except a date
    """
    dtime = value.to_datetime()
    dtime = (dtime - timedelta(hours=dtime.hour) - timedelta(minutes=dtime.minute) -
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
