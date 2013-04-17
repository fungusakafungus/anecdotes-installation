#!/usr/bin/env python
import subprocess
import time
import itertools
import glob
import sensor
import os

# here we will define some constants
STATE_START = "STATE_START"
STATE_LANDSCAPE_RUNNING = "STATE_LANDSCAPE_RUNNING"
STATE_PERSON_STARTING = "STATE_PERSON_STARTING"
STATE_PERSON_RUNNING = "STATE_PERSON_RUNNING"

EVENT_FINISHED = "EVENT_FINISHED"
EVENT_INCOMING = "EVENT_INCOMING"
EVENT_OUTGOING = "EVENT_OUTGOING"
EVENT_TIMEOUT = "EVENT_TIMEOUT"

START_TIMEOUT = 2.7




MY_PATH = os.path.dirname(__file__)
PLAYER = MY_PATH + "/omxplayer-simple"
VIDEO_PATH = MY_PATH + "/videos"
landscapes = glob.glob(VIDEO_PATH + "/L*")
persons = glob.glob(VIDEO_PATH + "/P*")
videofiles = zip(landscapes, persons)
videofiles = itertools.cycle(videofiles)
print videofiles.next()
print videofiles.next()
print videofiles.next()
print videofiles.next()



# here we will define so variables in the global scope which are used in the functions
person_started = None
last_sensor_state = None
person_process = None
landscape_process = None
landscapefile = None
personfile = None

state = STATE_START


def start_video(filename):
    return subprocess.Popen([PLAYER, filename], stdin=subprocess.PIPE)

def start_next_landscape():
    global landscapefile, personfile, landscape_process
    landscapefile, personfile = videofiles.next()
    landscape_process = start_video(landscapefile)
    
def start_person():
    global person_process, person_started
    person_process = start_video(personfile)
    person_started = time.time()

def kill_landscape():
    landscape_process.kill()
    
def error():
    print "Unexpected state: %s, event: %s" % (state, event)


while True:
    # TODO: check, if interrupt ends the program when in sleep()
    time.sleep(0.1)
    event = None
    current_time = time.time()
    if person_started and current_time - person_started > START_TIMEOUT:
        event = EVENT_TIMEOUT
    person_started = None
    new_sensor_state = sensor.state()
    if last_sensor_state != new_sensor_state:
        if new_sensor_state == True:
            event = EVENT_INCOMING
        else:
            event = EVENT_OUTGOING
    last_sensor_state = new_sensor_state
    if person_process and (person_process.poll() is not None):
        event = EVENT_FINISHED
        person_process = None
    if landscape_process and (landscape_process.poll() is not None):
        event = EVENT_FINISHED
        landscape_process = None
    
    #print "event: ", event
    #print "state: ", state
    if state == STATE_START:
        start_next_landscape()
        print "lanscape process when starting:", landscape_process
        state = STATE_LANDSCAPE_RUNNING
    if not event:
        continue
    # TODO: if person video is running, do not start next landscape video
    elif state == STATE_LANDSCAPE_RUNNING:
        if event == EVENT_FINISHED:
            start_next_landscape()
            state = STATE_LANDSCAPE_RUNNING
        elif event == EVENT_INCOMING:
            start_person()
            state = STATE_PERSON_STARTING
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
