# INFO
# Plot received data from serial port
# User input COM and baud rate with exceptions if error
#
# QUICK START
# 1) Flash microcontroller board with operational code
# 2) Press and hold reset button microcontroller board to begin transmittion
# 3) Transmitter: check for flashing red light on radio telemetry air module to confirm data being sent
# 4) Receiver: check for solid green light on radio telemetry ground module to confirm pair with transmitter
# 5) Operator: smile when you receive data
#
# Raymond Yu
# Plotter created with assistance
# 20 January 2019

import sys
import serial
import time
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#import seaborn

plt.style.use("ggplot") # pre-defined style

baudRateList = [110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000]

def livePlotter(x_vec, y1_data, line1, identifier = '', pause_time = 0.1):

    if line1 == []:
        plt.ion() # set interactive plotting
        fig = plt.figure(figsize = (12,6)) # set size of display
        ax = fig.add_subplot(2, 2, 1) # 1x1 graph, 1st position. 2, 3, 4 = 2x3 graph, 4th position.

        #create a variable for the line so we can update later
        line1, = ax.plot(x_vec, y1_data, '-o', alpha = 0.5)
        plt.ylabel('Voltage (mV)')
        plt.xlabel('Time (s)')
        plt.title('Bat_1'.format(identifier))
        plt.show()

    #after we only update y data
    line1.set_ydata(y1_data)
    # #adjust limits if new data goes out of bounds
    # if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
    #     plt.ylim([np.min(y1_data)-np.std(y1_data),
    #               np.max(y1_data)+np.std(y1_data)])
    plt.ylim(-100, 5000)

    #pause to let the axis/figure catch up
    plt.pause(pause_time)

    #return the line so we can reuse it
    return line1

def getUserInput():
    print("*** Read serial data from COM port ***")
    targetSerialPort = input("Enter COM port (e.g. COM14): ")
    baudRate = int(input("Enter baud rate: ")) # convert input string to integer

    # Remove all white spaces from COM import else error
    targetSerialPort = targetSerialPort.replace(' ', '')

    # Check if a correct baud rate entered
    if baudRate not in baudRateList:
        print("Error: Incorrect baud rate entered.")
        sys.exit(1) # exit program
    return targetSerialPort, baudRate

def parseData(inputData):
    warning1, warning2, warning3 = (' ', ' ', ' ')
    stringSplit = inputData.split(' ') # split input data by char

    bat1 = stringSplit[1] # assign depending on location
    bat2 = stringSplit[3]
    aoa = stringSplit[5]
    ss = stringSplit[7]

    try:
        if (int(bat1) < 500) or (int(bat2) < 500):
            warning1 = 'BATT WARNING'
        if int(aoa) > 100:
            warning2 = 'AOA WARNING'
        if int(ss) > 120:
            warning3 = 'SIDESLIP WARNING'
    except ValueError:
        pass
    return bat1, bat2, aoa, ss, warning1, warning2, warning3

targetSerialPort, baudRate = getUserInput()

try:
    serialPort = serial.Serial(targetSerialPort, baudRate, \
        bytesize = serial.EIGHTBITS, \
        parity = serial.PARITY_NONE, \
        stopbits = serial.STOPBITS_ONE, \
        timeout = 1, \
        xonxoff = False, \
        rtscts = False)
except serial.serialutil.SerialException: # serial port inaccessible error
    print("Serial port cannot be found. Check COM port or if it is open in another program.")
    sys.exit(1)

#testdata
size = 10
x_vec = np.linspace(-60,0,size+1)[0:-1]
y_vec = np.zeros(10)
line1=[]

while True:
    try:
        data = serialPort.readline()
        Bat_1, Bat_2, AoA, Sideslip, Warning1, Warning2, Warning3 = parseData(str(data,'utf-8').strip('\r\n'))

        # Plot graph
        y_vec[-1] = Bat_1 # input data here
        line1 = livePlotter(x_vec, y_vec, line1)
        y_vec = np.append(y_vec[1:], 0.0) # what does this do?
        # print(len(y_vec))

        # print("Bat_1: " + Bat_1 + "V" \
        #     + "\t" + "Bat_2: " + Bat_2 + "V" \
        #     + "\t" + "AoA: " + AoA + "degs" \
        #     + "\t" + "Sideslip: " + Sideslip + "degs"
        #     + "\t" + Warning1 + "\t" + Warning2 + "\t" + Warning3)
    except ValueError:
        pass
    except IndexError:
        pass
    except UnicodeDecodeError: # check if data can be decoded
        print("Unable to decode. Check baud rate.")
        break
    except KeyboardInterrupt: # means to stop program
        print("Program stopped.")
        break

serialPort.flush()
serialPort.close()
