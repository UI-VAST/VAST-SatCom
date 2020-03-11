#!/usr/bin/python
import time

class Iridium():
    def __init__(self):
        self.ring = "SBDRING"
        # +SBDIX:<MO stat>,<MOMSN>,<MT stat>,<MTMSN>,<MT length>,<MT queued>
        self.sbdi = "+SBDIX: 0,0,1,0,8,0"
        self.sbdrt = "+SBDRT: hello world"
        self.msg = ""
        self.in_waiting = 0

    def write(self,str):
        if(str == "AT+SBDIXA\r\n"):
            time.sleep(1)
            self.msg = self.sbdi
        elif(str == "AT+SBDRT\r\n"):
            time.sleep(1)
            self.msg = self.sbdrt
        self.in_waiting = len(self.msg)

    def readline(self):
        str = self.msg
        self.msg = ""
        self.in_waiting = 0
        return str

    def begin(self):
        time.sleep(1)
        self.msg = self.ring
        self.in_waiting = len(self.msg)

