#!/usr/bin/python

import iridium
import time

port = "/dev/ttyUSB0"
baud = 19200
ir = iridium.Iridium(port,baud)
sq = ir.csq()

countdown = 0
# set interval to time between sending packets in seconds.
# should be like 60 or 90.
# 5 for testing.
# also, come up with a better variable name than interval.
interval = 5

try:
    while 1:
        # if ring activated,
        # check for message.
        if(ir.ring()):
            print("message received")
            while(sq < 1):
                sq = ir.csq()
            status = ir.SBDI()
            # if return status bad,
            # check again till it's good.
            while(status > 8):
                status = ir.SBDI()
            msg = ir.readSBD()
            print("message: " + msg)
        # if countdown exceeds interval,
        # reset interval and send out a packet.
        if(countdown > interval):
            countdown = 0
            print("send")
            #ir.writeSBD("outgoing message")
            #ir.SBDI()
        countdown += 1
        time.sleep(1)
        print(countdown)

except(KeyboardInterrupt,SystemExit):
    ir.stop()
