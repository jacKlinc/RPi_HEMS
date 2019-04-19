from matplotlib import pyplot, dates
import numpy as np
import pandas as pd
import scipy.signal as signal
import peakutils

missing_values = ["-"]


def get_d(my_csv):      # pass CSV file, get demand
    raw_csv = pd.read_csv(my_csv, sep=',', na_values=missing_values)
    day_alloc = raw_csv.iloc[0:len(raw_csv):,1]
    day_alloc = day_alloc.real.astype(int)
    time_x1 = np.arange(0, len(day_alloc)/4, 0.25)
    return day_alloc

def get_t(my_t):        # # pass CSV file, get time axis
    raw_t = pd.read_csv(my_t, sep=',', na_values=missing_values)
    day_alloc = raw_csv.iloc[0:len(raw_t):,1]
    time_x1 = np.arange(0, len(day_alloc)/4, 0.25)
    return time_x1


def make_day(day_x, raw_c):
    c = get_d(raw_c)
    if day_x <= 0 or day_x >= len(c)/24:
        print("enter valid value")
    else:
        return c[(day_x-1)*96 : ((day_x-1)*96)+96] # 96/4 = 24 hours in a day

def make_index(what_day):
    return peakutils.indexes(make_day(what_day), thres=0.8, min_dist=10)
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

make_plot(1, 'go', 'Demand_3.csv')
pyplot.title('Peaks over month')
pyplot.xlabel('Time/hours')
pyplot.ylabel('Demand/MW')
pyplot.show()
# make_plot(2, 'yo')
# make_plot(3, 'ro')
# make_plot(4, 'bo')
# make_plot(5, 'bo')

# print(len(y1))

#pyplot.plot(x1, y1)


# print(peak_avg(2, 2))
