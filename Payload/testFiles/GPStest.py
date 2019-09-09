#!/usr/bin/python

import serial
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

venus = serial.Serial("/dev/ttyS0",baudrate=9600,timeout=5)
#gpsFile = open("./gpslog.txt","a")

while 1:
    nmeaString = venus.readline()
    print(nmeaString)
    #gpsFile.write(nmeaString)
    venus.reset_input_buffer()
    venus.flush()
    time.sleep(3)
