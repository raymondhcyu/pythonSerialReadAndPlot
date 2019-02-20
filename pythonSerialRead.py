# INFO
# Read and receive data from serial port and print to console_output
# Print serial only; for plotting see other file
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
# 19 January 2019

import os
import sys
import serial
import time
import numpy as np
import datetime

baudRateList = [110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000]
fullVoltage = 25.0
emptyVoltage = 20.0
aoa = beta = bat1 = bat2 = [0.0]
warning = [None] * 4 # four possible warnings
warningVoltagePercentage = ((21.0 - emptyVoltage)/(fullVoltage - emptyVoltage)) * 100
AoAWarningAngle = 100.0
sideslipWarningAngle = 200.0
oldVoltage = [0.0] # check for failure
newVoltage = [0.0] # check for failure

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
    try:
        stringSplit = inputData.split(',') # split input data by char

        # Parsing
        time = stringSplit[0] # first float is time, synced to transmitter
        sg = np.zeros(8)
        for i in range(len(sg)):
            sg[i] = stringSplit[(i + 1)]
        aoa[0] = stringSplit[9]
        beta[0] = stringSplit[10]
        bat1[0] = ((float(stringSplit[11]) - emptyVoltage)/(fullVoltage - emptyVoltage)) * 100 # scale and turn to percentage
        bat2[0] = ((float(stringSplit[12]) - emptyVoltage)/(fullVoltage - emptyVoltage)) * 100 # scale and turn to percentage
        newVoltage = [bat1]

        oldVoltage = newVoltage.copy()

        # Anomaly checks
        if (float(bat1[0]) < warningVoltagePercentage) or (float(bat2[0]) < warningVoltagePercentage):
            warning[0] = 'BATT WARNING'
        if float(aoa[0]) > AoAWarningAngle:
            warning[1] = 'AOA WARNING'
        if float(beta[0]) > sideslipWarningAngle:
            warning[2] = 'SIDESLIP WARNING'
        # if oldVoltage[0] != 0 and (newVoltage[0] > (oldVoltage[0] * 1.01)):
        #     warning[3] = 'ENGINE WARNING'

    except IndexError: # if data corruption pass error
        pass
    except ValueError: # if data corruption pass error
        pass
    return time, sg, aoa, beta, bat1, bat2, warning

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
    sys.exit(1) # exit program

# Prepare text file to write data to, e.g. 2019_01_22_23_17_59.txt
currentDT = datetime.datetime.now()
file = open("FT_" + currentDT.strftime("%Y_%m_%d_%H_%M_%S") + ".txt", "w")
file.write("Time" + "\t" + "SG1" + "\t" + "SG2" + "\t" + "SG3" + "\t" + "SG4" \
    + "\t" + "SG5" + "\t" + "SG6" + "\t" + "SG7" + "\t" + "SG8" \
    + "\t" + "AoA" + "\t" + "Beta" + "\t" + "Bat_1" + "\t" + "Bat_2")

while True:
    try:
        data = serialPort.readline() # read from serial port
        os.system("cls") # clear previous lines
        # print(str(data,'utf-8').strip('\r\n')) # read data and remove carriage returns and newlines
        Time, SG, AoA, Sideslip, Bat_1, Bat_2, Warning = parseData(str(data,'utf-8').strip('\r\n'))

        SG = [str(i) for i in SG] # convert array elements to string
        Warning = [str(i) for i in Warning]
        AoA = [str(i) for i in AoA]
        Sideslip = [str(i) for i in Sideslip]
        Bat_1 = [str(i) for i in Bat_1]
        Bat_2 = [str(i) for i in Bat_2]

        # Print to user console
        print("Uptime: " + Time \
            + "\t" + "SG1: " + SG[0] \
            + "\t" + "SG2: " + SG[1] \
            + "\t" + "SG3: " + SG[2] \
            + "\t" + "SG4: " + SG[3] \
            + "\t" + "SG5: " + SG[4] \
            + "\t" + "SG6: " + SG[5] \
            + "\t" + "SG7: " + SG[6] \
            + "\t" + "SG8: " + SG[7] \
            + "\t" + "AoA: " + AoA[0] \
            + "\t" + "Sideslip: " + Sideslip[0] \
            + "\t" + "Bat_1: " + Bat_1[0] \
            + "\t" + "Bat_2: " + Bat_2[0])

        # Print warnings; auto new line
        if Warning[0]:
            print(Warning[0])
        if Warning[1]:
            print(Warning[1])
        if Warning[2]:
            print(Warning[2])
        # if Warning[3]:
        #     print(Warning[3])

        # Write to text file; auto new line
        file.write("\n" + Time + "\t" + SG[0] + "\t" + SG[1] + "\t" + SG[2] + "\t" + SG[3] + "\t" \
            + SG[4] + "\t" + SG[5] + "\t" + SG[6] + "\t" + SG[7] + "\t" \
            + AoA[0] + "\t" + Sideslip[0] + "\t" + Bat_1[0] + "\t" + Bat_2[0])

    except IndexError:
        pass
    except UnicodeDecodeError: # check if data can be decoded
        print("Unable to decode. Check baud rate.")
        break
    except KeyboardInterrupt: # means to stop program
        print("Program stopped.")
        break

file.close()
# Clean and close serial port for future use
serialPort.flush()
serialPort.close()
