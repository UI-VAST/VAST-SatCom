#!/usr/bin/python

from Iridium import iridium
import time
import datetime

# program to automatically transmit data over iridium network.

#TODO:
'''
    in separate script, record gps data into a gps logger.
    do this every 1 second.
    every time iridium transmits, pull only latest gps data from that file
    to send.
    
    do the same for other data, temperature, air pressure, etc.

    handle receiving of cutdown command.
'''

port = "/dev/ttyS0"
#port = "/dev/ttyUSB0"
baud = 19200

ir = iridium.Iridium(port,baud)
ir.transmissionTime = 90	# transmit every 90 seconds
ir.dest = "RB0012851"	#make sure you know which iridium modem is sending, which is receiving

iridium.log("session started at " + iridium.timestamp())

# ir.listen() begins the listener on a separate thread.  
#anything coming in from Iridium will be read and processed, 
#including the SBDRING indicating that a message has come in.
ir.listen()

packet = ''

while 1:
    # when transmissionTime seconds have passed, do the thing.
    # and reset countdown timer
    if(ir.countdown > ir.transmissionTime):
        ir.SBDWT(packet)
        ir.countdown = 0
    time.sleep(1)
