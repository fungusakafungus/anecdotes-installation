#!/usr/bin/env python
import subprocess
import time
import itertools
import glob
import sensor
import ultrasonic
import os
from ConfigParser import ConfigParser
import logging
import logging.handlers

import gapless_player

# here we will define some constants
STATE_START = "STATE_START"
STATE_LANDSCAPE_RUNNING = "STATE_LANDSCAPE_RUNNING"
STATE_PERSON_RUNNING = "STATE_PERSON_RUNNING"

EVENT_INCOMING = "EVENT_INCOMING"
EVENT_OUTGOING = "EVENT_OUTGOING"
EVENT_FINISHED = "EVENT_FINISHED"

MY_PATH = os.path.dirname(__file__)
PLAYER = MY_PATH + "/omxplayer-simple"
VIDEO_PATH = MY_PATH + "/videos"
landscapes = sorted(glob.glob(VIDEO_PATH + "/L*"))
persons = sorted(glob.glob(VIDEO_PATH + "/P*"))
videofiles = zip(landscapes, persons)
videofiles = itertools.cycle(videofiles)

# here we will define the variables in the global scope which are used in functions
person_started = None
last_sensor_state = None
last_player_state = None
landscapefile = None
personfile = None

state = STATE_START

def start_video(filename):
    logger.info("starting %s", filename)
    gapless_player.play(filename)

def start_next_landscape():
    global landscapefile, personfile
    landscapefile, personfile = videofiles.next()
    start_video(landscapefile)

def start_person():
    start_video(personfile)

def error():
    logger.error("Unexpected state: %s, event: %s", state, event)

def read_config():
    config = ConfigParser()
    config.readfp(open(MY_PATH + '/config-default.ini'))
    config.read(MY_PATH + "/config.ini")
    return config

def configure_logging():
    config = read_config()
    logger = logging.getLogger()
    logger.level = logging.DEBUG
    syslog_host = config.get("anecdotes", "syslog_host")
    handler = logging.handlers.SysLogHandler(address=(syslog_host, 514), facility=logging.handlers.SysLogHandler.LOG_LOCAL0)
    formatter = logging.Formatter('%(asctime)s %(name)s: %(levelname)s %(message)s', '%b %e %H:%M:%S')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

# configure logging
logger = configure_logging()

try:
    while True:
        time.sleep(0.1)
        # re-read the distance config (config.ini) to make tuning easier
        sensor.read_config()
        event = None
        new_sensor_state = sensor.state()
        if last_sensor_state != new_sensor_state:
            if new_sensor_state == True:
                event = EVENT_INCOMING
            else:
                event = EVENT_OUTGOING
        last_sensor_state = new_sensor_state

        new_player_state = gapless_player.is_stopped()
        if last_player_state != new_player_state:
            logger.info("player_state changed:  %s", new_player_state)
            if new_player_state == False:
                pass
            else:
                logger.info("player_state finished:  %s", new_player_state)
                event = EVENT_FINISHED
        last_player_state = new_player_state

        if state == STATE_START and event != EVENT_INCOMING:
            start_next_landscape()
            state = STATE_LANDSCAPE_RUNNING
        if not event:
            continue
        logger.debug("event:  %s", event)
        logger.debug("state:  %s", state)
        # TODO: if person video is running, do not start next landscape video
        if state == STATE_LANDSCAPE_RUNNING:
            if event == EVENT_INCOMING:
                start_person()
                state = STATE_PERSON_RUNNING
            elif event == EVENT_OUTGOING:
                pass
            elif event == EVENT_FINISHED:
                start_next_landscape()
                state = STATE_LANDSCAPE_RUNNING
            else:
                error()
        elif state == STATE_PERSON_RUNNING:
            if event == EVENT_INCOMING:
                pass
            elif event == EVENT_OUTGOING:
                start_next_landscape()
                state = STATE_LANDSCAPE_RUNNING
            elif event == EVENT_FINISHED:
                start_next_landscape()
                state = STATE_LANDSCAPE_RUNNING
            else:
                error()
except Exception, e:
    logger.exception(e)
finally:
    ultrasonic.quit()
    gapless_player.quit()
