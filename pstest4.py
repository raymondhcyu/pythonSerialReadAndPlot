# Read and receive data from serial port and print to console_output
# Print serial only; for plotting see other file
#
# Raymond Yu
# 19 January 2019

import serial
import time

targetSerialPort = input("Enter COM port (e.g. COM14): ")
baudRate = int(input("Enter baud rate: "))

# serialPort = serial.Serial(targetSerialPort, baudRate, timeout = 1)

print(targetSerialPort, type(targetSerialPort))
print(baudRate, type(baudRate))

while True:
    try:
        print("Hey there!")
        time.sleep(1)
    except KeyboardInterrupt:
        print("Program exiting")
        break

# serialPort.flush()
# serialPort.close()
