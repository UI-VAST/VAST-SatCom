#!/usr/bin/python

from logger import *
from Iridium import iridium
import time

# program to receive incoming data over iridium network.

port = "/dev/ttyS0"
baud = 19200

ir = iridium.Iridium(port,baud)
ir.dest = "RB0012828"

iridium.log("session started at " + iridium.timestamp())

ir.listen()

while 1:
	if(ir.LastMessage != ""):
		#do something with the data that came in.
		print("got: " + ir.LastMessage)
		ir.LastMessage = ""
	time.sleep(1)
