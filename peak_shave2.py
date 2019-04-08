import plotly.plotly as py
import plotly.graph_objs as go
from matplotlib import pyplot, dates

import numpy as np
import pandas as pd
import scipy.signal as signal
import peakutils

my_data = pd.read_csv('Demand_3.csv', sep=',') #usecols=['DATE']
#my_data = my_data.set_index('DATE & TIME')
my_data = my_data.rename(columns={'DATE':'DATETIME'}) # rename


date = my_data.iloc[1:601,0]
demand = my_data.iloc[1:601:,1]

demand = demand.real.astype(int)
#demand = demand.real.astype(int)

#print(type(demand))
#print(type(date[2]))
#print(date[2])

#for i in date:
 #   date[i] = date[i][13:18]

#peaks = signal.find_peaks_cwt(demand, np.arange(100,200))
window = signal.general_gaussian(51, p=0.5, sig=20)
filtered = signal.fftconvolve(window, demand)
filtered = (np.average(demand) / np.average(filtered)) * filtered
peaks = np.roll(filtered, -25)


pyplot.plot(peaks, 'b--', demand, 'r')
pyplot.title('Demand over Time')
pyplot.xlabel('Time/15mins')
pyplot.ylabel('Demand/MW')
pyplot.show()