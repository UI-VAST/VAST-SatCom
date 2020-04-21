#!/usr/bin/python

import serial
import time
import pynmea2
import os
import datetime
import threading

def timestamp():
    return str(datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S"))

#venusGPS = serial.Serial("/dev/ttyUSB0",baudrate=9600,timeout=5)
venusGPS = serial.Serial("/dev/ttyS0",baudrate=9600,timeout=5)

logPath = os.path.join(os.getcwd(),'log')
if(not os.path.exists(logPath)):
    os.mkdir(logPath)
gpsFile = os.path.join(logPath,'gps' + timestamp() + '.txt')

# nmea:
# $GPGGA,timestamp,lat,n,lon,w,fix,numsats,hdop,altitude,m,geoid,m,time,dgps,checksum
def begin():
    venusGPS.reset_input_buffer()
    venusGPS.flush()
    while 1:
        nmeaString = venusGPS.readline()
        #print(nmeaString)
        try:
            pynmea2.parse(nmeaString)
            with open(gpsFile,'a') as f:
                f.write(nmeaString)

            venusGPS.reset_input_buffer()
            venusGPS.flush()
            time.sleep(3)
        except:
            continue

            '''
            nmeaParsed = pynmea2.parse(nmeaString);

            '''

def GetLatestGPS():
    with open(gpsFile,'r') as f:
        for latest in f:
            pass
    return latest

# this file is imported in IridiumTransmitter.py,
# which runs the entire file,
# and launches this thread:
threading.Thread(target=begin).start()
