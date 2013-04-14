#!/usr/bin/env python
import subprocess
import time
import itertools
import glob
import sensor

PLAYER = "/home/pi/show/omxplayer-simple"
landscapes = glob.glob("/home/pi/videos/L*")
persons = glob.glob("/home/pi/videos/P*")
videofiles = zip(landscapes, persons)
oldprocess = None
print sensor.state()
for landscapefile, personfile in itertools.cycle(videofiles):
    process = subprocess.Popen([PLAYER, landscapefile], stdin=subprocess.PIPE)
    while process.poll() == None:
        time.sleep(0.1)
        if sensor.state():
            personprocess = subprocess.Popen([PLAYER, personfile], stdin=subprocess.PIPE)
            time.sleep(2.7)
            if oldprocess and not oldprocess.poll():
                oldprocess.terminate()
    oldprocess = process
