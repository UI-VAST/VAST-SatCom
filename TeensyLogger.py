#!/usr/bin/python

'''
    reads in data from Teensy (ext. and int. temperature sensors),
    and from MPL pressure sensor (which also contains an internal temp).
    outputs data to teensyPacketFile
    ....
    this should be renamed, since it's not only reading from the Teensy.
'''

import smbus
import time
import MPL

teensy = smbus.SMBus(1)
teensyAddr = 0x04
mplAddr = 0x60

teensyPacketFile = '/home/uivast/data/teensyPackets.txt';
teensyLast = '/home/uivast/data/teensyLast.txt';

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
        altitude += str(MPL.getAltitudeM())
        print(altitude)
    except:
        print("can't read altitude .")
        altitude = "-127"
    
    data += extTemp + "," + intTemp + "," + altitude + "," + pressure
    with open(teensyPacketFile,'a') as f:
        f.write(data + '\n')
    with open(teensyLast,'w') as f:
        f.write(data) 
    time.sleep(3)

