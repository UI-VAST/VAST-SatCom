#!/usr/bin/python

from Iridium import iridium
import time
import datetime

# program to receive incoming data over iridium network.

port = "/dev/ttyS0"
baud = 19200

ir = iridium.Iridium(port,baud)
ir.dest = "RB0012828"

iridium.log("session started at " + timestamp())

ir.listen()

while 1:
	if(ir.LastMessage != ""):
		#do something with the data that came in.
		print("got: " + ir.LastMessage)
		ir.LastMessage = ""
	time.sleep(1)
