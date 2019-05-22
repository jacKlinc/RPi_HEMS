import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import time

miss_val = '-'
# Dates
d = dt.date(2019, 3, 2)
today = dt.date.today()
t_delta = today - d


# Convert to datetime
time_format = '%H:%M:%S'
#dt_strip = dt.datetime.strptime(nice_format, date_format) # takes the string, its format
#print(dt_strip)


raw_t = pd.read_csv('Demand_3.csv', sep=',', na_values=miss_val)

#raw_t['DATE'] = pd.to_datetime(raw_t['DATE'])


print(type(raw_t['DATE'][2]))
#raw_t['DATE'] = raw_t['DATE'].dt.time
demand = pd.to_numeric(raw_t['DEMAND'])



#raw_t['DATE'] = raw_t['DATE'].dt.time


raw_t.index = pd.to_datetime(raw_t.DATE, dayfirst=True)
#plt.plot('DEMAND', data=raw_t)
#plt.show()


######### it plots but need to cut datetime to day, hour, min
#print(raw_t['DEMAND']) # there was a space in the .csv



user@laptop:~$ sudo apt-get update
user@laptop:~$ sudo apt-get upgrade
