#!/usr/bin/python

import serial
import time

ir = serial.Serial("/dev/ttyUSB0",baudrate=19200,timeout=5)


ir.write("AT+CSQ\r")
time.sleep(0.5)
r = ir.readline()
while(r[:5] != '+CSQ:'):
    r = ir.readline()
    print r
#r = r.split(":")[1].strip()
print r

exit()
