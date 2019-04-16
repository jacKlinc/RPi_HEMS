from matplotlib import pyplot, dates
import numpy as np
import pandas as pd
import scipy.signal as signal
import peakutils

missing_values = ["-"]

my_data = pd.read_csv('Demand_3.csv', sep=',') 
demand = my_data.iloc[15:591:,1]
demand = demand.real.astype(int)
time_x = np.arange(0, 24, 0.25)

my_data1 = pd.read_csv('Month_D.csv', sep=',', na_values=missing_values)
demand1 = my_data1.iloc[0:2784:,1]
demand1 = demand1.real.astype(int)
time_x1 = np.arange(0, len(demand1)/4, 0.25)


def make_day(day_x):
    if day_x <= 0 or day_x >= len(demand)/24:
        print("enter valid value")
    else:
        return demand[(day_x-1)*96 : ((day_x-1)*96)+96] # 96/4 = 24 hours in a day

def make_index(what_day):
    return peakutils.indexes(make_day(what_day), thres=0.8, min_dist=10)
    # passed day array, 80% thres, xdist=10

def make_plot(day, col):                    # day, colour of peak
    pyplot.plot(time_x, make_day(day))      # main plot
    pyplot.plot(                            # peaks
        time_x [ make_index(day) ],         # xpeak
        make_day(day) [ make_index(day) ],  # ypeak
        col                                 # color of peak
    )
    return 1

def peak_avg(p_day, peak_r):        # day, peak range
    peak = []
    for i in range(0, peak_r):
        peak.append(make_index(p_day)[i])
    return np.mean(peak)/4

#make_plot(1, 'go')
# make_plot(2, 'yo')
# make_plot(3, 'ro')
# make_plot(4, 'bo')
# make_plot(5, 'bo')

print(len(demand))

#pyplot.plot(time_x, demand)
pyplot.title('Peaks over month')
pyplot.xlabel('Time/hours')
pyplot.ylabel('Demand/MW')
pyplot.show()

# print(peak_avg(2, 2))
