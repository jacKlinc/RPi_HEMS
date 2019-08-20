from matplotlib import pyplot, dates
import numpy as np
import pandas as pd
from pandas import DatetimeIndex as dti
import peakutils
import datetime as dt


missing_values = ["-"]

# #make_plot(1, 'go', 'Demand_3.csv')
# pyplot.title('Peaks over month')
# pyplot.xlabel('Time/hours')
# pyplot.ylabel('Demand/MW')
# #pyplot.show()

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

def is_peak(data_series): # date_t needs to be pydatetime
    demand_s = get_demand(data_series)
    date_series = get_date(data_series)

    for val in demand_s:
        if val != "NaN":
            demand_s = np.array(list(map(int, demand_s))) 
        else: 
            del val
    
    
    peak_times = peakutils.indexes(demand_s, thres=0.8, min_dist=10)

    # peak_vals = []                       # stores the peaks values
    # for idx, j in enumerate(peak_times):
    #     peak_vals.append(i_series[j])   # the peaks at the given indexes

    return peak_times

#my_date = dt.datetime(2019, 3, 2)
x = is_peak('Month_D.csv')
print("")
print(x)
print("")

