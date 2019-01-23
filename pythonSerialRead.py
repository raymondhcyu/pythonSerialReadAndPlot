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

# def parseData(inputData):
#     return None

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

while True:
    try:
        data = serialPort.readline()
        os.system("cls")
        print(str(data,'utf-8').strip('\r\n')) # read data and remove carriage returns and newlines
        # None = parseData(str(data,'utf-8').strip('\r\n'))

        # add future functionality to detect if no data being received
        # print(data) # start, stop, carriage return, and quotes still attached
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
