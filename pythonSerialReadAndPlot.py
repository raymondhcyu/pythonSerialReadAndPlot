

import collections
import serial
import threading
import time
import numpy as np
from itertools import islice
import matplotlib.pyplot as plt
import matplotlib.animation as animation

x = np.linspace(-100, 0, 1000) # make 1,000 points evenly distributed from -30 to 0
y = collections.deque([0]*1000, maxlen=1000) # initialize the y to have 1000 points in it, or matplotlib will complain if x and y are not the same size


def in_background():
    serialport = serial.Serial("COM14", 57600, timeout=0.5)

    while True:
            command = serialport.readline()
            console_output = str(command,'utf-8').strip('\r\n')
            if console_output != "":
                y.append(console_output)
                print(console_output)
    serialport.close()

thread = threading.Thread(target = in_background)
thread.start()

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
line, = ax1.plot(x, y)

def animate(i):
    line.set_ydata(y)

ani = animation.FuncAnimation(fig, animate, interval=200)
plt.ylim(0, 2000)
plt.show()
