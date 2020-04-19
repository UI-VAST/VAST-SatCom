#!/usr/bin/python

'''
    class for Iridium 9602 modem.
    relies on asserting SBDRING to receive incoming message.

'''

from logger import *
import serial
import time
import threading

#Iridium class:
class Iridium:
    def __init__(self,port,baud):
        self.port = serial.Serial(port,baudrate=baud,timeout=5)
        self.port.reset_input_buffer()
        self.port.flush()
        self.write("AT+SBDREG\r\n")
        time.sleep(1)
        self.countdown = 0
        self.transmissionTime = 90
        self.sq = 0
        self.dest = ""
        self.LastMessage = ""
        #self.csq()

    def listen(self):
        threading.Thread(target=self.CheckMessages).start()

    # just writes to serial port
    def write(self,msg):
        log(msg)
        self.port.write(msg)

    # writes message to outgoing buffer
    def SBDWT(self,msg):
        if(self.dest != ""):
            msg = self.dest + msg
        self.write("AT+SBDWT=" + msg + "\r\n")

    # reads from incoming buffer
    def SBDRT(self):
        self.write("AT+SBDRT\r\n")

    # initiate SBD session
    def SBDI(self,alert=False):
        log("initiating session....")
        if(alert):
            self.write("AT+SBDIXA\r\n")
        else:
            self.write("AT+SBDIX\r\n")

    # just reads from serial port
    def read(self):
        return self.port.readline()

    # checks signal quality.
    # sending CSQ appears to interrupt any other command in progress.
    # also appears to prevent SBDRING from coming in.
    # maybe come up with a better way to check signal.
    # but if we handle network connection errors internally (see SBDI: response in ProcessPackets())
    # we don't necessarily need to confirm signal quality.
    def csq(self):
        #print("checking signal....")
        #pass
        self.write("AT+CSQ\r\n")
        '''
        r = ""
        while("CSQ:" not in r):
            r += self.read()
        print("SQ: " + r.split(":")[1])
        return int(r.split(":")[1])
        '''

    def available(self):
        return self.port.in_waiting

    def CheckMessages(self):
        log("listener started");
        # infinite loop running in second thread
        while 1:
            #print('reading')
            if(self.available() > 0):
                r = []
                print("reading")
                while(self.available() > 0):
                    r.append(self.port.readline()) 
                self.ProcessPacket(r)
            time.sleep(1)
            #print(self.countdown);
            self.countdown += 1
        return r

    def ProcessPacket(self,packet):
        log("packet:")
        log(packet)
        for i,p in enumerate(packet):
            if("CSQ:" in p):
                self.sq = int(p[5])
                log("sq:"+str(self.sq));
                                # every time a csq packet comes in,
                                # check sq again.
                #self.csq()
            if("SBDIX:" in p):
                response = p.split(":")[1].split(",");
                mo = response[0]
                mt = response[2]
                log("mo:" + mo);
                log("mt:" + mt);
                if(int(mo) > 4):
                    self.SBDI()
                    log("message not sent, tryin again")
                else:
                    log("message sent")
                    self.write("AT+SBDD0\r\n")
                    time.sleep(1)
                    #self.csq()
                if(int(mt) > 1):
                    self.SBDI(alert=True)
                    log("no service, trying again")
                elif(int(mt) == 1):
                    log("message got")
                    self.SBDRT()
                else:
                    log("no messages at gateway")
            if("SBDWT" in p):
                self.SBDI()
            if("SBDRING" in p):
                log(p)
                self.SBDI(alert=True)
            if("SBDRT:" in p):
                log("message received!\n" + packet[i+1])
                self.LastMessage = packet[i+1]
                self.write("AT+SBDD1\r\n")
                time.sleep(1)



