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


class WWLN(object):
    """Deal with WWLN data"""

    def Gen_date(filename):
        ''' Generate the datetime object from a filename string'''
        yr = int(filename.split('.')[0][1:5])
        mth = int(filename.split('.')[0][5:7])
        day = int(filename.split('.')[0][7:9])
        return dt.datetime(yr, mth, day)


if __name__ == "__main__":
    print("Executing lightning_analysis.py directly")
