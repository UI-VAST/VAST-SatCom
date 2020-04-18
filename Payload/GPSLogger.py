#!/usr/bin/python

import serial
import time
import pynmea2

#venusGPS = serial.Serial("/dev/ttyUSB0",baudrate=9600,timeout=5)
venusGPS = serial.Serial("/dev/ttyS0",baudrate=9600,timeout=5)

gpsPacketFile = '/home/uivast/data/gpsPackets.txt';
gpsLastLine = '/home/uivast/data/gpsLastLine.txt';

# nmea:
# $GPGGA,timestamp,lat,n,lon,w,fix,numsats,hdop,altitude,m,geoid,m,time,dgps,checksum
venusGPS.reset_input_buffer()
venusGPS.flush()
while 1:
    nmeaString = venusGPS.readline()
    print(nmeaString)
    if(pynmea2.parse(nmeaString)):
        with open(gpsPacketFile,'a') as f:
            f.write(nmeaString + '\n')
        with open(gpsLastLine,'w') as f:
            f.write(nmeaString)

        venusGPS.reset_input_buffer()
        venusGPS.flush()
        time.sleep(3)

        '''
        nmeaParsed = pynmea2.parse(nmeaString);

        '''
