import os
import numpy as np
import pandas as pd
import datetime as dt


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
    hh, mm, sec_micro = tvals.split(':')
    hh = int(hh)
    mm = int(mm)
    ss, mss = sec_micro.split('.')
    ss = int(ss)
    mss = int(mss)
    return dt.datetime(*dvals, hh, mm, ss, mss)

if __name__ == "__main__":
    print("Executing lightning_analysis.py directly")
