# Doodle and test-test space

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# def simplePlot():
#     # Data for plotting
#     t = np.arange(0.0, 2.0, 0.01) # 0 to 2 in 0.01 intervals, aka array of 200 steps
#     s = np.sin(2 * np.pi * t) # returns sine of each input
#
#     fig, ax = plt.subplots()
#     ax.plot(t, s)
#
#     ax.set(xlabel='time (s)', ylabel='voltage (mV)', title='About as simple as it gets, my dudes')
#     ax.grid()
#
#     fig.savefig("test.png")
#     plt.show()
#     return None
#
# simplePlot()

# print(np.zeros(100))
# print(len(np.zeros(100)))


# string = 'Bat_1: 639 Bat_2: 739 AoA: 63 Sideslip: 73 \nSG1: 904 SG2: 1004 SG3: 1104 SG4: 1204 SG5: 904 SG6: 1004 SG7: 1104 SG8: 1204'
# print("Original string: " + string, type(string))
#
# stringSplit = string.split(' ')
# # print(stringSplit)
# Bat_1 = stringSplit[1]
# Bat_2 = stringSplit[3]
# AoA = stringSplit[5]
# Sideslip = stringSplit[7]
#
# SG = np.zeros(8)
#
# for i in range(len(SG)):
#     SG[i] = stringSplit[(i + 9 + (i % 2) * 2)]
#
# SG[0] = stringSplit[9]
# SG[1] = stringSplit[11]
# SG[2] = stringSplit[13]
# SG[3] = stringSplit[15]
# SG[4] = stringSplit[17]
# SG[5] = stringSplit[19]
# SG[6] = stringSplit[21]
# SG[7] = stringSplit[23]
#
# print("Bat_1: " + Bat_1 + "V")
# print("Bat_2: " + Bat_2 + "V")
# print("AoA: " + AoA + "degs")
# print("Sideslip: " + Sideslip + "degs")
#
# # Change to for loop
# for i in range(len(SG)):
#     print("SG" + str(i) + ": " + str(SG[i]) + "V")

for i in range(8):
    print(i, i + 9 + (i % 2))
