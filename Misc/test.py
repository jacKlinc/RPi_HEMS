import math
import matplotlib.pyplot as plt
import numpy as np

x = np.array([0,1,2,3,4,5,6,7,8,9,10])
y = list()

for idx, i in enumerate(x):
    y.append(2**idx)

y = np.array(y)

plt.plot(x,y)
plt.show()
