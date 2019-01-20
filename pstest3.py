# Simple plot

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# def simplePlot():
#     # Data for plotting
#     t = np.arange(0.0, 2.0, 0.01)
#     s = 1 + np.sin(2 * np.pi * t)
#
#     fig, ax = plt.subplots()
#     ax.plot(t, s)
#
#     ax.set(xlabel='time (s)', ylabel='voltage (mV)', title='About as simple as it gets, folks')
#     ax.grid()
#
#     fig.savefig("test.png")
#     plt.show()
#     return None
#
# simplePlot()

string = 'Bat_1: 639 Bat_2: 739 AoA: 63 Sideslip: 73 SAMPLE WARNING'
print("Original string: " + string, type(string))

stringSplit = string.split(' ')
# print(stringSplit)
Bat_1 = stringSplit[1]
Bat_2 = stringSplit[3]
AoA = stringSplit[5]
Sideslip = stringSplit[7]

print("Bat_1: " + Bat_1 + "V")
print("Bat_2: " + Bat_2 + "V")
print("AoA: " + AoA + "degs")
print("Sideslip: " + Sideslip + "degs")
