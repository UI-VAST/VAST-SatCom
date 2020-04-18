#!/usr/bin/python

import smbus
import time
import MPL
import RPi.GPIO as GPIO

teensy = smbus.SMBus(1)
teensyAddr = 0x04
mplAddr = 0x60

teensyPacketFile = '/home/uivast/data/teensyPackets.txt';
teensyLast = '/home/uivast/data/teensyLast.txt';

cutdownAltitude = 22000 # meters
#meters     feet
# 25000     82021
# 27432     90000
# 30000     98425
# 30480     100000

cutdownAltitudeCount = 0
cutdownPin = 12
isCutdown = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(cutdownPin,GPIO.OUT)

def cutDown():
    cd = GPIO.PWM(cutdownPin,10)
    cd.start(1)
    time.sleep(4)

while 1:
    data = ""
    extTemp = ""
    pressure = ""
    altitude = ""
    intTemp = ""

    print("reading ext temp ....")
    try:
        teensyData = teensy.read_i2c_block_data(teensyAddr,0)
        for c in teensyData:
            if c > 31 and c < 58:
                extTemp += chr(c)
        print(extTemp)
    except:
        print("can't read ext temp .")
        extTemp = "-127"

    print("reading int temp ....")
    try:
        intTemp += str(MPL.getTempC())
        print(intTemp)
    except:
        print("can't read int temp .")
        intTemp = "-127"

    print("reading pressure ....")
    try:
        pressure += str(MPL.getPressure())
        print(pressure)
    except:
        print("can't read pressure .")
        pressure = "-127"

    print("reading altitude ....")
    try:
        altInt = MPL.getAltitudeM()
        altitude += str(altInt)
        print(altitude)
        if(altInt > cutdownAltitude):
            cutdownAltitudeCount += 1
        else:
            cutdownAltitudeCount = 0
        if(cutdownAltitudeCount > 3):
            cutDown()
            isCutdown = True
    except:
        print("can't read altitude .")
        altitude = "-127"
    
    data += extTemp + "," + intTemp + "," + altitude + "," + pressure
    if(isCutdown):
        data += ",cutdown"
    with open(teensyPacketFile,'a') as f:
        f.write(data + '\n')
    with open(teensyLast,'w') as f:
        f.write(data) 
    time.sleep(3)


