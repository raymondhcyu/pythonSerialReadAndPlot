# Single plot, originally for Arduino
# Kinda works, occasionally plot stops completely with index error. 2s latency
# Move exceptions inside parseData? serial.readline outside of try/except seems to reduce latency

import serial
import matplotlib.pyplot as plt
from drawnow import *
import atexit

values = []

plt.ion()
cnt=0

data = serial.Serial("COM14", 57600)

def plotValues():
    plt.title('Bat_1 Voltage')
    plt.grid(True)
    plt.ylabel('Voltage (mV)')
    plt.plot(values, 'rx-', label='Voltage')
    plt.legend(loc='upper right')
    plt.ylim(-100, 5000)

def doAtExit():
    data.close()
    print("Close serial")
    print("data.isOpen() = " + str(data.isOpen()))

def parseData(inputData):
    warning1, warning2, warning3 = (' ', ' ', ' ')
    stringSplit = inputData.split(' ') # split input data by char

    bat1 = stringSplit[1] # assign depending on location
    # bat2 = stringSplit[3]
    # aoa = stringSplit[5]
    # ss = stringSplit[7]
    #
    # try:
    #     if (int(bat1) < 500) or (int(bat2) < 500):
    #         warning1 = 'BATT WARNING'
    #     if int(aoa) > 100:
    #         warning2 = 'AOA WARNING'
    #     if int(ss) > 120:
    #         warning3 = 'SIDESLIP WARNING'
    # except ValueError:
    #     pass
    return bat1 #, bat2, aoa, ss, warning1, warning2, warning3

atexit.register(doAtExit)

print("data.isOpen() = " + str(data.isOpen()))

#pre-load dummy data
for i in range(0,26):
    values.append(0)

while True:
    while (data.inWaiting()==0):
        pass

    valueRead = data.readline()
    Bat_1 = parseData(str(valueRead,'utf-8').strip('\r\n'))

    #check if valid value can be casted
    try:
        valueInInt = int(Bat_1)
        Bat_2 = AoA = Sideslip = Warning1 = Warning2 = Warning3 = 'Null'
        print("Bat_1: " + Bat_1 + "V" \
            + "\t" + "Bat_2: " + Bat_2 + "V" \
            + "\t" + "AoA: " + AoA + "degs" \
            + "\t" + "Sideslip: " + Sideslip + "degs"
            + "\t" + Warning1 + "\t" + Warning2 + "\t" + Warning3)
        if valueInInt <= 4096:
            if valueInInt >= 0:
                values.append(valueInInt)
                values.pop(0)
                drawnow(plotValues)
    except ValueError:
        print("Error: Cannot cast.")
        pass
    except IndexError:
        print("Error: Out of index.")
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
