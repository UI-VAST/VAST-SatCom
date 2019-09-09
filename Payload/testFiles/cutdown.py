#!/usr/bin/python

# tool to trigger linear actuator cutdown mechanism.
# usage:  include 'open' or 'close' as argument.  example:
# $: ./cutdown.py open

import RPi.GPIO as GPIO
import time
import sys

cutdownPin = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(cutdownPin, GPIO.OUT)

if(len(sys.argv) < 2):
    print("specify \'open\' or \'close\'");
    exit()

if(sys.argv[1] == 'open'):
    print("opening")
    cd = GPIO.PWM(cutdownPin,10)
    cd.start(1)
    time.sleep(3)
    exit()
elif(sys.argv[1] == 'close'):
    print("closing")
    cd = GPIO.PWM(cutdownPin,5)
    cd.start(1)
    time.sleep(3)
    exit()
