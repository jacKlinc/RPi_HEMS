from matplotlib import pyplot, dates
import numpy as np
import pandas as pd
from pandas import DatetimeIndex as dti
import scipy.signal as signal
import peakutils
import datetime as dt


missing_values = ["-"]

#make_plot(1, 'go', 'Demand_3.csv')
pyplot.title('Peaks over month')
pyplot.xlabel('Time/hours')
pyplot.ylabel('Demand/MW')
#pyplot.show()

def get_date(my_csv):      # pass CSV file, get demand
    raw_csv = pd.read_csv(my_csv, sep=',', na_values=missing_values)
    date_s = pd.to_datetime(raw_csv['DATE'])
    return date_s

def get_demand(my_csv):      # pass CSV file, get demand
    raw_csv = pd.read_csv(my_csv, sep=',', na_values=missing_values)
    demand_series = pd.to_numeric(raw_csv['DEMAND'])
    return demand_series

def make_plot(day, col, x_t):                    # day, colour of peak
    pyplot.plot(get_t(x_t), make_day(day, x_t))      # main plot
    pyplot.plot(                            # peaks
        get_t(x_t) [ make_index(day, x_t) ],         # xpeak
        make_day(day) [ make_index(day) ],  # ypeak
        col                                 # color of peak
    )
    return 1

def is_peak(data_series, date_chosen, demand): # date_t needs to be pydatetime
    demand_s = get_demand(data_series)
    date_series = get_date(data_series)

    day = date_series.dt.day

    demand_needed = []
    for idx, d in day.iteritems():
        if d == date_chosen.day:
            demand_needed.append(demand_s.iloc[idx])

    demand_needed = np.array(list(map(int, demand_needed))) # converts to int
    peak_times = peakutils.indexes(demand_needed, thres=0.8, min_dist=10) 
    # these only give the index of the peaks inside demand_needed

    peak_val = []   # stores the peaks 
    for idx, j in enumerate(peak_times):
        peak_val.append(demand_needed[j])   # the demands at the given indexes

    peak_avg = np.mean(peak_val)

    thresh = peak_avg - peak_avg/20
    if demand >= thresh:
        return True
    else:
        return False

my_date = dt.datetime(2019, 3, 2)
x = is_peak('Month_D.csv', my_date, 4100)
print(x)

