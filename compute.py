#!/usr/bin/python

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

data = np.genfromtxt('kv-gh-rot.csv', delimiter=',', names=True)
# print "2"
# print(type(data))
# print(matplotlib.backends.backend)
# plt.plot(data['time'], data['Z_value'])
# plt.show()

locX = []
locY = []

curX = 0.0
curY = 0.0

openList = []
finalTraj = []

# data['time'], data['Z_value']
for i in range(1, min(len(data['time']), len(data['Z_value'])) - 1):
	print data['time'][i], data['Z_value'][i]
	pass
