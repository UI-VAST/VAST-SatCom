#!/usr/bin/python

import pyridium
import time

iridium = pyridium.Iridium()

def ReadTxt():
    print("getting text")
    iridium.write("AT+SBDRT\r\n")
    time.sleep(1)
    msg = ""
    while("+SBDRT:" not in msg):
        msg += iridium.readline()
    print(msg)

def SbdSession():
    print("initiating session")
    iridium.write("AT+SBDIXA\r\n")
    time.sleep(1)
    msg = ""
    while("+SBDIX:" not in msg):
        msg = iridium.readline()
    packet = msg.split(',')
    if(packet[2] == '1'):
        ReadTxt()

def Listen():
    if(iridium.in_waiting > 0):
        msg = ""
        while(iridium.in_waiting > 0):
            msg += iridium.readline()
        if("SBDRING" in msg):
            print("ringing")
            SbdSession()

iridium.begin()
while 1:
    Listen()
    time.sleep(1)
