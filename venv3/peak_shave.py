from matplotlib import pyplot, dates
import numpy as np
import pandas as pd
from pandas import DatetimeIndex as dti
import peakutils
import datetime as dt
from influxdb import InfluxDBClient	
from influxdb import DataFrameClient

import influx_insert as ins

i_client = InfluxDBClient(host='localhost', port=8086) # set Grafana data source to this
i_client.switch_database('ozw4')			# change to database name

missing_values = ["-"]

def get_date(my_csv):      # pass CSV file, get demand
    raw_csv = pd.read_csv(my_csv, sep=',', na_values=missing_values)
    date_s = pd.to_datetime(raw_csv['DATE'])
    return date_s

def get_demand(my_csv):      # pass CSV file, get demand
    raw_csv = pd.read_csv(my_csv, sep=',', na_values=missing_values)
    demand_series = pd.to_numeric(raw_csv['DEMAND'])
    return demand_series

def make_plot(val, time_st, col):                    # value, datetime, colour of peak (plot value with datetime)
    pyplot.plot(val, range(len(val)))      # main plot
    pyplot.plot(                            # peaks
        get_t(x_t) [ make_index(day, x_t) ],         # xpeak
        make_day(day) [ make_index(day) ],  # ypeak
        col                                 # color of peak
    )
    return 1



def sort_data(d_series): # taking past hour of readings as takes panda df
  
    d_series = d_series.to_dict() # then to dictionary

    val_list = []                       # stores value
    #time_list = []
    for val in d_series.keys():      # keys are the index in this case
        val_list.append(d_series[val][0]['Value']) # makes list of values
        #time_list.append(data_series[val][0]['time'])

    return np.array(val_list) # convert list to numpy ndarray

def is_peak(i_series, demand):

    np_series = sort_data(i_series)
    peak_times = make_index(np_series)
    # these only give the index of the peaks inside demand_needed

    peak_vals = []                       # stores the peaks values
    for idx, j in enumerate(peak_times):
        peak_vals.append(i_series[j])   # the peaks at the given indexes

    peak_avg = np.mean(np_series)       
    print(peak_avg)
    thresh = peak_avg - peak_avg/20     # within 5% of avg

    if demand >= thresh:
        return True
    else:
        return False

def make_index(n_series):
    return peakutils.indexes(n_series, thres=0.8, min_dist=10) # ndarray
 
# pand = ins.to_panda()
# #print(x)

# y_ax = sort_data(pand)


# pyplot.plot(range(len(y_ax)), y_ax)      # main plot

# pyplot.plot(                            # peaks
#     make_index(y_ax),         # xpeak
#     make_day(day) [ make_index(day) ],  # ypeak
#     col                                 # color of peak
# )

# pyplot.show()




### time
#print(type(time_list[1][2]))
#no_t = time_list[1].rsplit('T', 1) #removes T
# no_z = no_t[1].rsplit('Z', 1) # and Z
# pure_date = no_t[0] + no_z[0]
# print(type(pure_date))
# my_date = dt.datetime.strptime(pure_date, '%Y-%m-%d%H:%M:%S.%f')
# 2019-05-07T13:46:30.387777082Z