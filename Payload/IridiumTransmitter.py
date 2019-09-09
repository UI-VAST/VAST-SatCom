#!/usr/bin/python

import serial
import time
import datetime
import pynmea2
import RPi.GPIO as GPIO


# connect the Ring Indicator (RI) pin on Iridium to pin 16 on pi.
# actually, don't; the iridium unit pushes SBDRING 
# through serial port when RI is enabled.

RI = 16     
address = "RB0012851";
iridium = serial.Serial("/dev/ttyUSB0",baudrate=19200,timeout=3)
cutdown = False
cutdownPin = 12
cutdownAltitude = 25000 # meters
# meters    feet
# 25000     82021
# 27432     90000
# 30000     98425
# 30480     100000
cutdownAltitudeCount = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RI,GPIO.IN)
GPIO.setup(cutdownPin,GPIO.OUT)

logFile = '/home/uivast/data/logfile.log'
gpsFile = '/home/uivast/data/gpsLastLine.txt'
teensyFile = '/home/uivast/data/teensyLast.txt'

# every txTime seconds, send a message
txTime = 60 
txCountDown = txTime 


def log(string):
    print(string)
    with open(logFile,'a') as f:
        f.write(str(datetime.datetime.now()) + '\t')
        f.write(str(string) + '\n')

def newMessage():
    return not GPIO.input(RI)

def Signal():
    log("checking iridium network status")
    iridium.write("AT+CSQ\r")
    time.sleep(0.1)
    r = iridium.readline()
    while(r[:5] != '+CSQ:'):
        r = iridium.readline()
        time.sleep(0.1)
    log(r)
    r = r.split(":")[1].strip()
    return r != '0'

def checkRI():
    log("checking Ring Indicator")
    if(iridium.in_waiting):
        log("message at port")
        while(iridium.in_waiting):
            r = iridium.readline()
            log(r)
            if("SBDRING" in r):
                log("Ring Indicator activated\n")
                log("initiating sbd session\n")
                iridium.write("AT+SBDIXA\r")
                time.sleep(0.1)
                r = iridium.readline()
                while("+SBDIX:" not in r):
                    log(r)
                    time.sleep(0.1)
                    r = iridium.readline()
                log(r)
                if(r.split(',')[2] == ' 1'):
                    log("received text\n")
                    irReceive()

def irReceive():
    iridium.write("AT+SBDRT\r")
    time.sleep(0.1)
    r = iridium.readline()
    while("+SBDRT:" not in r):
        r = iridium.readline()
        log(r)
    r = iridium.readline()
    log(r)
    if('cutdown' in r):
        cutdown = True
        cutDown()


def cutDown():
    log("cutting down")
    cd = GPIO.PWM(cutdownPin,10)
    cd.start(1)
    time.sleep(4)


def irTransmit(packet):
    log("writing packet to modem")
    iridium.write("AT+SBDWT=" + address + ',' + packet + '\r');
    '''
    iridium.write("AT+SBDWT" + '\r')
    time.sleep(1)
    response = ''
    while(response != "READY\r\n"):
        response = iridium.readline()
        log(response)
        time.sleep(0.1)

    log(address + ',' + packet + '\r');
    iridium.write(address + ',' + packet + '\r')
    '''
    time.sleep(0.1)
    response = ''
    while("OK" not in response):
        response = iridium.readline()
        log(response)
        time.sleep(0.1)

    log("transmitting packet")
    iridium.write("AT+SBDI\r")
    time.sleep(1)

    while("+SBDI:" not in response):
        response = iridium.readline()
        log(response)
    if(response.split(',')[2] == ' 1'):
        log("message waiting")
        irReceive()
    if(response[7] == '1'):
        log("packet successfully transmitted.")
        return True
    else:
        log("error transmitting.")
        return False



log('\n\n' + str(datetime.datetime.now()) + '\tNew Session')

nmea = ''
nmeaFull = ''
teensyString = ''
while 1:
    checkRI()
    packet = ''

    #while not Signal():
        #time.sleep(0.5)
    txCountDown += 1
    log(txCountDown)
    if(txCountDown >= txTime):
        txCountDown = 0
        log("getting latest GPS string")
        with open(gpsFile,'r') as f:
            nmeaFull = f.readline().strip()

        # packet will not contain full NMEA string.  format will be comma separated value (CSV):
        # iridium address, timestamp, latitude, N, longitude, W, altitiude, M
        # example:
        # RB0012851,14:22:33,4633.000,N,11723.000,W,827.4,M,24.0,22.0,notCutdown
        # when dashboard is updated, uncomment this section and comment out next section.
        try:
            nmea = pynmea2.parse(nmeaFull,check=False)
            packet += nmea.timestamp.strftime("%H:%M:%S") + ',' + nmea.lat + ',' + nmea.lat_dir + ',' + nmea.lon + ',' + nmea.lon_dir + ',' + str(nmea.altitude) + ',' + nmea.altitude_units + ','
        except:
            nmea = "00:00:00,0.0,N,0.0,W,0.0,M,"

        #packet += nmeaFull + ','
        # then get temp, pressure, append to packet.  and whether is cutdown or not.

        log("getting latest teensy data")
        with open(teensyFile,'r') as f:
            teensyString = f.readline().strip()
        packet += teensyString + ','
        # check if altitude above cutdownAltitude
        if(float(teensyString.split(',')[3]) > cutdownAltitude and not cutdown):
            log("altitude: " + teensyString.split(',')[3])
            cutdownAltitudeCount += 1
        elif(float(teensyString.split(',')[3]) < cutdownAltitude and not cutdown):
            cutdownAltitudeCount = 0
        if(cutdownAltitudeCount > 3):
            cutdown = True
            cutDown()

        if(iridium.in_waiting):
            checkRI()
        if(cutdown):
            packet += 'cutdown'
        else:
            packet += 'notCutdown'

        log("packet: " + packet)
        success = irTransmit(packet)
        if(not success):
            txCountDown = txTime
    
    time.sleep(1)
