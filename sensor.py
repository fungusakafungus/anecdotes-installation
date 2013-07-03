from __future__ import division
import sys
import os
from ConfigParser import ConfigParser
import collections
import logging

logger = logging.getLogger("sensor")

try:
    import RPi.GPIO as GPIO
    import ultrasonic
    GPIO.setwarnings(False)

except ImportError:
    GPIO = None
    import getch
    print "looks like we are not running on a raspberry pi!"

MY_PATH = os.path.dirname(__file__)

OUTGOING = False
INCOMING = True
WINDOW_SIZE = None
distances = None

last_state = OUTGOING

def read_config():
    global MIN_DISTANCE, MAX_DISTANCE, WINDOW_SIZE, distances
    config = ConfigParser()
    config.readfp(open(MY_PATH + '/config-default.ini'))
    config.read(MY_PATH + "/config.ini")
    MIN_DISTANCE = config.getint("anecdotes", "min_distance")
    MAX_DISTANCE = config.getint("anecdotes", "max_distance")
    new_window_size = config.getint("anecdotes", "window_size")
    if WINDOW_SIZE != new_window_size:
        WINDOW_SIZE = new_window_size
        distances = collections.deque(maxlen=WINDOW_SIZE)
        
    

def state():
    global last_state
    if GPIO:
        current_distance = ultrasonic.distance()
        # the sensor can only measure up to 4 meters, so we skip too big values
        if not current_distance or current_distance > 450:
            return last_state
        distances.append(current_distance)
        l = sorted(list(distances))
        index = int(len(l) / 2)
        distance = l[index]
        state_str = "P" if last_state else "L"
        logger.info("distance: (%d/%d/%d) %s % 4.1f % 4.1f", MIN_DISTANCE, MAX_DISTANCE, WINDOW_SIZE, state_str, distance, current_distance)
        if last_state == INCOMING and distance > MAX_DISTANCE:
            last_state = OUTGOING
            return OUTGOING
        if last_state == OUTGOING and distance < MIN_DISTANCE:
            last_state = INCOMING
            return INCOMING
        return last_state
    else:
        # TODO: make a button
        try:
            with open("/tmp/trigger", 'r') as f:
                contents = f.read()
                return "incoming" in contents
        except:
            return False

read_config()
