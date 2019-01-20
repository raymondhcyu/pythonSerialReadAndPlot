# Read and receive data from serial port and print to console_output
# Print serial only; for plotting see other file
#
# User input COM and baud rate with exceptions if error
#
# Raymond Yu
# 19 January 2019

import sys
import serial
import time

baudRateList = [110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000]

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

def parseData(bat1, bat2, aoa, ss):

    return bat1, bat2, aoa, ss

targetSerialPort, baudRate = getUserInput()

try:
    serialPort = serial.Serial(targetSerialPort, baudRate, timeout = 1)
except serial.serialutil.SerialException: # serial port inaccessible error
    print("Serial port cannot be found. Check COM port or if it is open in another program.")
    sys.exit(1) # exit program

while True:
    try:
        data = serialPort.readline()

        # print(data) # start, stop, carriage return, and quotes still attached
        # print(str(data,'utf-8').strip('\r\n')) # read data and remove carriage returns and newlines
    except UnicodeDecodeError: # check if data can be decoded
        print("Unable to decode. Check baud rate.")
        break
    except KeyboardInterrupt: # means to stop program
        print("Program stopped.")
        break

# Clean and close serial port for future use
serialPort.flush()
serialPort.close()
