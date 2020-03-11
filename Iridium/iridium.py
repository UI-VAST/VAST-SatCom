#!/usr/bin/python

'''
    class for Iridium 9602 modem.
'''

import serial
import time
import threading
import RPi.GPIO as GPIO

done = False

class Iridium:
    def __init__(self,port,baud):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.port = serial.Serial(port,baudrate=baud,timeout=5)
        self.port.flush()
        self.RI = 16
        GPIO.setup(self.RI,GPIO.IN)
        print("setup complete")

    # just writes to serial port
    def write(self,msg):
        self.port.write(msg)

    # writes message to outgoing buffer
    def writeSBD(self,msg):
        self.write("AT+SBDWT=" + msg + "\r\n")
        r = ""
        while("OK" not in r):
            r = self.port.readline()

    # reads from incoming buffer
    def readSBD(self):
        self.write("AT+SBDRT\r\n")
        r = ""
        while("SBDRT:" not in r):
            r += self.port.readline()
        return r

    # initiate SBD session
    def SBDI(self):
        print("initiating session....")
        self.write("AT+SBDIXA\r\n")
        r = ""
        while("SBDIX:" not in r):
            r = self.port.readline()
            print(r)
        code = r.split(":")[1].split(",")
        status = int(code[0])
        # field 2 of return code indicates whether there's 
        # a message waiting.
        MTstatus = int(code[2])
        # do something with readSBD() here.
        if(MTstatus == 1)
            pass
        return status
        
    # just reads from serial port
    def read(self):
        return self.port.readline()

    # checks signal quality.
    def csq(self):
        print("checking signal...")
        self.write("AT+CSQ\r\n")
        r = ""
        while("CSQ:" not in r):
            r += self.port.readline()
        print("SQ: " + r.split(":")[1])
        self.port.flush()
        return int(r.split(":")[1])
    
    # polls Ring Indicator (RI) pin.
    # RI pin is active low.
    def ring(self):
        return not GPIO.input(self.RI)

    # kills threads.
    def stop(self):
        global done
        done = True
