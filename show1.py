#!/usr/bin/env python
import subprocess
import time
import itertools
import glob
import sensor

STATE_LANDSCAPE_RUNNING = 1
STATE_PERSON_STARTING = 2
STATE_PERSON_RUNNING = 3

EVENT_FINISHED = 5
EVENT_INCOMING = 6
EVENT_OUTGOING = 7
EVENT_TIMEOUT = 8

START_TIMEOUT = 2.7

PLAYER = "/home/pi/show/omxplayer-simple"
landscapes = glob.glob("videos/L*")
persons = glob.glob("videos/P*")
videofiles = zip(landscapes, persons)
videofiles = itertools.cycle(videofiles):

def start_video(filename):
    return subprocess.Popen([PLAYER, filename], stdin=subprocess.PIPE)

def start_next_landscape():
    landscapefile, personfile = videofiles.next()
    landscape_process = start_video(landscapefile)
    
def start_person():
    person_process = start_video(personfile)
    person_started = time.time()

def kill_landscape():
    landscape_process.kill()
    
def error():
    print "Unexpected state: %s, event: %s" % (state, event)

while True:
    time.sleep(0.1)
    current_time = time.time()
    if current_time - person_started > START_TIMEOUT:
        event = EVENT_TIMEOUT
    new_sensor_state = sensor.state()
    if last_sensor_state != new_sensor_state:
        if new_sensor_state == True:
            event = EVENT_INCOMING
        else:
            event = EVENT_OUTGOING
    last_sensor_state = new_sensor_state
    if person_process
            
        

if state == STATE_LANDSCAPE_RUNNING:
    if event == EVENT_FINISHED:
        start_next_landscape()
        state = STATE_LANDSCAPE_RUNNING
    elif event == EVENT_INCOMING:
        start_person()
        state = STATE_PERSON_STARTING:
    elif event == EVENT_OUTGOING:
        state = STATE_LANDSCAPE_RUNNING
    elif event == EVENT_TIMEOUT:
        error()
    else:
        error()
elif state == STATE_PERSON_STARTING:
    if event == EVENT_FINISHED:
        start_next_landscape()
        state = STATE_LANDSCAPE_RUNNING
    elif event == EVENT_INCOMING:
        state = STATE_PERSON_STARTING
    elif event == EVENT_OUTGOING:
        start_next_landscape()
        state = STATE_LANDSCAPE_RUNNING
    elif event == EVENT_TIMEOUT:
        kill_landscape()
        state = STATE_PERSON_RUNNING
    else:
        error()
elif state == STATE_PERSON_RUNNING:
    if event == EVENT_FINISHED:
        start_next_landscape()
        state = STATE_LANDSCAPE_RUNNING
    elif event == EVENT_INCOMING:
        state = STATE_PERSON_RUNNING
    elif event == EVENT_OUTGOING:
        start_next_landscape()
        state = STATE_LANDSCAPE_RUNNING
    elif event == EVENT_TIMEOUT:
        error()
    else:
        error()
    
        
# states: start, landscape running, landscape stopping, person running, person stopping
# events: landscape finished, incoming 
