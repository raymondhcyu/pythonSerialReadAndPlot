# INFO
# Read and receive data from serial port and print to console_output
# Input data format: "float float float float float float float float float" space deliminated
# Print serial only; for plotting see other file
#
# USER INPUTS
# - COM port
# - Baud baud
# - ctrl+c to stop program
#
# QUICK START
# 1) Flash microcontroller board with operational code
# 2) Press and hold reset button microcontroller board to begin transmittion
# 3) Transmitter: check for flashing red light on radio telemetry air module to confirm data being sent
# 4) Receiver: check for solid green light on radio telemetry ground module to confirm pair with transmitter
# 5) Operator: smile when you receive data
#
# Raymond Yu
# 22 January 2019

import os
import sys
import serial
import time
import numpy as np

baudRateList = [110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000]

def getUserInput():
    print("*** Read serial data from COM port: SG Calibration ***")
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
    try:
        stringSplit = inputData.split(' ') # split input data by char
        time = stringSplit[0] # first float is time, synced to transmitter
        sg = np.zeros(8)
        for i in range(len(sg)):
            sg[i] = stringSplit[(i + 1)]
    except IndexError: # if data corruption pass error
        pass
    except ValueError: # if data corruption pass error
        pass
    return time, sg

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

while True:
    try:
        data = serialPort.readline() # read from serial port
        os.system("cls") # clear previous lines
        # print(str(data,'utf-8').strip('\r\n')) # Testpoint: read data and remove carriage returns and newlines
        Time, SG = parseData(str(data,'utf-8').strip('\r\n'))
        SG = [str(i) for i in SG]

        print("Uptime: " + Time \
            + "\t" + "SG1: " + SG[0] \
            + "\t" + "SG2: " + SG[1] \
            + "\t" + "SG3: " + SG[2] \
            + "\t" + "SG4: " + SG[3] \
            + "\t" + "SG5: " + SG[4] \
            + "\t" + "SG6: " + SG[5] \
            + "\t" + "SG7: " + SG[6] \
            + "\t" + "SG8: " + SG[7] \
        )
        # add future functionality to detect if no data being received
    except IndexError:
        pass
    except UnicodeDecodeError: # check if data can be decoded
        print("Unable to decode. Check baud rate.")
        break
    except KeyboardInterrupt: # means to stop program
        print("Program stopped.")
        break

# Clean and close serial port for future use
serialPort.flush()
serialPort.close()
