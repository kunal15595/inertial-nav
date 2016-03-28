#!/usr/bin/python

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
data = np.genfromtxt('kv-gh-rot.csv', delimiter=',', names=True)
# print "2"
print(type(data))
print(matplotlib.backends.backend)
# plt.plot(data['time'], data['Z_value'])
# plt.show()

locX = []
locY = []

curX = 0.0
curY = 0.0

for i in range(1, min(len(data['time']), len(data['Z_value'])) - 1):
	# print data['time'][i], data['Z_value'][i]
	curX +=  (data['time'][i] - data['time'][i-1]) * np.sin(np.deg2rad(data['Z_value'][i]+14.5))
	curY +=  (data['time'][i] - data['time'][i-1]) * np.cos(np.deg2rad(data['Z_value'][i]+14.5))
	# print curLoc
	locX.append(curX)
	locY.append(curY)


# print loc[0,:]
plt.plot(locX, locY, marker='.', color='r', ls='')
# plt.xlim(-200, 200)
# plt.ylim(-200, 200)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
