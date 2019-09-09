#!/usr/bin/python

from __future__ import print_function
import RPi.GPIO as GPIO
import time
import serial

RI = 16
ir = serial.Serial("/dev/ttyS0",baudrate=19200,timeout=2)
timestamp = 0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RI,GPIO.IN)


ring = GPIO.input(RI)


# every 1 second, read the Ring Indicator pin
# to check for a new message.

while(1):
    ring = GPIO.input(RI)
    print("ring: ",end='')
    print(ring)

    if(ring == 0):
        ir.write("AT+SBDIX\r")
        time.sleep(0.5)
        r = ir.readline().split(',')
        while("+SBDIX:" not in r[0]):
            r = ir.readline().split(',')
            print(r)
            time.sleep(0.1)
        if(r[2] == ' 1'):
            ir.write("AT+SBDRT\r")
            time.sleep(0.5)
            r = ir.readline()
            while("+SBDRT:" not in r):
                print(r)
                r = ir.readline()
            r = ir.readline()
            print(r)


    time.sleep(0.75)

    # send signal Check Ring Indicator Status:
    '''
    ir.write("AT+CRISX\r")
    r = ir.readline()
    r = ir.readline().split(',')
    print(r)
    while("+CRISX" not in r[0]):
        r = ir.readline().split(',')
        print(r)

    sri = int(r[1])
    newTime = int(r[2],16)
    print(newTime)

    # if SBD Ring Indicator is 1, and if the timestamp is something new, output and update timestamp
    if(sri == 1 and newTime != timestamp):
        print('message received')
        messageReceived = True
        timestamp = newTime
    else:
        print('no new messages.')

    while "OK" not in r:
        r = ir.readline()
    print()
    r = ir.readline()

    if(r == 'SBDRING'):
        ir.write("AT+SBDIX\r")
        r = ir.readline()
        while "OK" not in r:
            r = ir.readline()
        ir.write("AT+SBDRT\r")
        r = ir.readline()
        while "OK" not in r:
            print(r)
            r = ir.readline()
        messageReceived = False
    '''
