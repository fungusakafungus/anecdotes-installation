#!/usr/bin/python
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|-|S|p|y|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# ultrasonic_1.py
# Measure distance using an ultrasonic module
#
# Author : Matt Hawkins
# Date   : 09/01/2013

# Import required Python libraries
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO = 24

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Allow module to settle
time.sleep(0.5)

reset = 0
def distance():
    global reset

    current_time = time.time()
    if current_time - reset < 0.06:
        return None
    reset = current_time

    # Send 10us pulse to trigger
    #print "Send 10us pulse to trigger"
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    #print "waiting for GPIO_ECHO to become 1"
    if GPIO.input(GPIO_ECHO)==0:
        while GPIO.input(GPIO_ECHO)==0:
            if start > reset + 1:
                print "timeout waiting for GPIO_ECHO to become 1"
                return None
            start = time.time()

    stop = time.time()
    #print "waiting for GPIO_ECHO to become 0"
    while GPIO.input(GPIO_ECHO)==1:
        if stop > reset + 1:
            print "timeout waiting for GPIO_ECHO to become 0"
            return None
        stop = time.time()

    # Calculate pulse length
    elapsed = stop-start

    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000

    # That was the distance there and back so halve the value
    distance = distance / 2

    #print "Distance : %.1f" % distance

    # Set trigger to False (Low)
    GPIO.output(GPIO_TRIGGER, False)
    return distance

def quit():
    GPIO.cleanup()
