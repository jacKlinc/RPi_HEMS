import numpy as np
from matplotlib import pyplot, dates
from csv import reader
import scipy.signal
from dateutil import parser
import datetime as dt

with open('Eirgrid_Demand2.csv', 'r') as f:  # must be in same dir
    data = list(reader(f))                  # makes a list of all data

parser.parse('2015-08-20 23:58:30')         # this converts string to datetime obj

print(type(data[1][0]))
print(data[1][0])

date_time_obj = dt.datetime.strptime(data[1][0], '%H:%M:%S')

dates_list = [dt.datetime.strptime(i[0], '%H:%M:%S').date() for date in dates]
#time =          [i[0] for i in data[1::]]   # this picks 0th column without title
act_demand =    [i[1] for i in data[1::]]   # 1st, [1::] removes 0th row
#pred_demand =   [i[2] for i in data[1::]]   # 2nd
'''
pyplot.plot(time, act_demand, 'r--')
pyplot.title('Demand over Time')
pyplot.xlabel('Time/hours')
pyplot.ylabel('Demand/MW')
pyplot.show()
'''



'''
##### 
names = ['group_a', 'group_b', 'group_c']
values = [1, 10, 100]

print('Detect peaks with order (distance) filter.')
indexes = scipy.signal.argrelextrema(
    np.array(vector),
    comparator=np.greater,order=2
)
plt.plot(vector)
plt.show()
print('Peaks are: %s' % (indexes[0]))

plt.figure(1, figsize=(9, 3))

plt.subplot(131)
plt.bar(names, values)
plt.subplot(132)
plt.scatter(names, values)
plt.subplot(133)
plt.plot(names, values)
plt.suptitle('Categorical Plotting')
plt.show()

#### using annotations
ax = plt.subplot(111)

t = np.arange(0.0, 5.0, 0.01)
s = np.cos(2*np.pi*t)
line, = plt.plot(t, s, lw=2)

plt.annotate('peak', xy=(2, 1), xytext=(3, 1.5),
             arrowprops=dict(facecolor='black', shrink=0.05),
             )

plt.ylim(-2, 2)
plt.show()

'''