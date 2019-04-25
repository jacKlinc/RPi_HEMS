from matplotlib import pyplot, dates
import numpy as np
import pandas as pd
from pandas import DatetimeIndex as dti
import scipy.signal as signal
import peakutils
import datetime as dt


missing_values = ["-"]


def get_d(my_csv):      # pass CSV file, get demand
    raw_csv = pd.read_csv(my_csv, sep=',', na_values=missing_values)
    demand_s = pd.to_numeric(raw_csv['DEMAND'])
    date_s = pd.to_datetime(raw_csv['DATE'])
    #date_s[''] = pd.DatetimeIndex(date_s.year)

    #demand = demand.real.astype(int)
    #time_x1 = np.arange(0, len(day_alloc)/4, 0.25)
    return date_s

def make_day(day_x, raw_c):
    c = get_d(raw_c)
    if day_x <= 0 or day_x >= len(c)/24:
        print("enter valid value")
    else:
        return c[(day_x-1)*96 : ((day_x-1)*96)+96] # 96/4 = 24 hours in a day

def make_index(what_day, c_csv):
    return peakutils.indexes(make_day(what_day, c_csv), thres=0.8, min_dist=10)
    # passed day array, 80% thres, xdist=10

def make_plot(day, col, x_t):                    # day, colour of peak
    pyplot.plot(get_t(x_t), make_day(day, x_t))      # main plot
    pyplot.plot(                            # peaks
        get_t(x_t) [ make_index(day, x_t) ],         # xpeak
        make_day(day) [ make_index(day) ],  # ypeak
        col                                 # color of peak
    )
    return 1

def peak_avg(p_day, peak_r):        # day, peak range
    peak = []
    for i in range(0, peak_r):
        peak.append(make_index(p_day)[i])
    return np.mean(peak)/4

#make_plot(1, 'go', 'Demand_3.csv')
pyplot.title('Peaks over month')
pyplot.xlabel('Time/hours')
pyplot.ylabel('Demand/MW')
#pyplot.show()


def get_peaks(date_c, date_t): # date_t needs to be pydatetime
    raw_csv = pd.read_csv(date_c, sep=',', na_values=missing_values)
    demand_s = pd.to_numeric(raw_csv['DEMAND'])
    date_series = pd.to_datetime(raw_csv['DATE'])
    
    day_in_series = date_s.dt.to_pydatetime().date
    day_passed = date_t.date
    peak = []
    #if day_in_series == day_passed:


    
    # now get peaks for that day
    #for i in demand_s:
    return array_of_peaks


# date_t = 'some date'
# peak_s = get_peaks('Demand_3.csv', date_t)
# print(type(peak_s))

date = get_d('Demand_3.csv')
print(type(date[2]))