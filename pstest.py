

import sys, serial
import numpy as np
from time import sleep
from collections import deque
from matplotlib import pyplot as plt

# class that holds analog data for N samples
class AnalogData:
  # constr
  def __init__(self, maxLen):
    self.ax = deque([0.0]*maxLen)
    self.maxLen = maxLen

  # ring buffer
  def addToBuf(self, buf, val):
    if len(buf) < self.maxLen:
      buf.append(val)
    else:
      buf.pop()
      buf.appendleft(val)

  # add data
  def add(self, data):
    assert(len(data) == 1)
    self.addToBuf(self.ax, data[0])

# plot class
class AnalogPlot:
  # constr
  def __init__(self, analogData):
    # set plot to animated
    plt.ion()
    self.axline, = plt.plot(analogData.ax)
    plt.ylim([0, 400])

  # update plot
  def update(self, analogData):
    self.axline.set_ydata(analogData.ax)
    plt.draw()

# main() function
def main():
  # expects 1 arg - serial port string
  # if(len(sys.argv) != 2):
  #   print('Example usage: python showdata.py "/dev/tty.usbmodem411"')
  #   exit(1)
  #
  # # strPort = '/dev/ttyUSB13'
  # strPort = sys.argv[1];

  # plot parameters
  analogData = AnalogData(100)
  analogPlot = AnalogPlot(analogData)

  print('plotting data...')

  # open serial port
  ser = serial.Serial('COM14', 57600)

  # print(ser)

  while True:
    try:
      line = ser.readline()
      try:
        data = [float(val) for val in line.split()]
        # print(data)
        if(len(data) == 1):
          analogData.add(data)
          analogPlot.update(analogData)
      except:
        # skip line in case serial data is corrupt
        pass
    except KeyboardInterrupt:
      print('exiting')
      break
  # close serial
  ser.flush()
  ser.close()

# call main
if __name__ == '__main__':
  main()
