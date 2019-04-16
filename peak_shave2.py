from matplotlib import pyplot, dates
import numpy as np
import pandas as pd
import scipy.signal as signal
import peakutils

my_data = pd.read_csv('Demand_3.csv', sep=',') #usecols=['DATE']

demand = my_data.iloc[15:591:,1]
demand = demand.real.astype(int)
time_x = np.arange(96)

def make_day(x):
    if x <= 0 or x >= len(demand)/96:
        print("enter valid value")
    else:
        return demand[x*96 : (x*96)+96]     # 96/4 = 24 hours in a day

def make_index(what_day):
    return peakutils.indexes(make_day(what_day), thres=0.8, min_dist=10)
    # passed day array, 80% thres, xdist=10

def make_plot(day, col):
    pyplot.plot(time_x, make_day(day))      # main plot
    pyplot.plot(                            # peaks
        time_x [ make_index(day) ],         # xpeak
        make_day(day) [ make_index(day) ],  # ypeak
        col                                 # color of peak
    )
    return 1

def peak_avg(p_day, peak_n, peak_r):
    peak = []
    for i in range(0, peak_r):
        peak.append(make_index(p_day)[i])
    return np.mean(peak)/4


make_plot(1, 'go')
make_plot(2, 'yo')
make_plot(3, 'ro')
make_plot(4, 'bo')

print(peak_avg(4, 1, 4))

# print(peak_avg(1, 1, 4)) # 1 is the first day, 1 is the first peak, 5 is the range


# pyplot.title('Demand over 5 Days')
# pyplot.xlabel('Time/15mins')
# pyplot.ylabel('Demand/MW')
# pyplot.show()


# https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html
# https://peakutils.readthedocs.io/en/latest/reference.html


'''window = signal.general_gaussian(51, p=0.5, sig=20) 
 51-no. of points in O/P, p=0.5-Laplace, sig-std deviation,   p=1-Gaussian
filtered = signal.fftconvolve(window, demand)
filtered = (np.average(demand) / np.average(filtered)) * filtered
peaks = np.roll(filtered, -35)
my_data = my_data.rename(columns={'DATE':'DATETIME'}) # rename

date = my_data.iloc[1:601,0]'''