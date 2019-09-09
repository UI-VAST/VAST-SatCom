#!/usr/bin/python

# allows user to interact directly with iridium 9602 modem.
# 

import serial
import time

iridium = serial.Serial("/dev/ttyUSB0",baudrate=19200,timeout=5)
iridium.reset_input_buffer()
iridium.flush()

while 1:
    command = raw_input("Enter AT Command: ")
    if command == 'exit':
        exit()
    iridium.write(command + "\r\n")
    time.sleep(1)
    response = ''
    while iridium.in_waiting or ('OK' not in response and 'ERROR' not in response): 
        response += iridium.readline()
    print(response)

