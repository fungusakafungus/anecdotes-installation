import os
import subprocess
import threading
import time
import logging

#MY_PATH = os.path.dirname(__file__)
#PLAYER = MY_PATH + "/omxplayer-simple"
PLAYER = './omxplayer-simple'

logging.basicConfig(level=logging.WARNING)

def start_video(filename):
    process = subprocess.Popen([PLAYER, filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    logging.debug("started %s: %s", filename, process)
    return process

old_process = None
process = None
start_delay = 0.8
check_every = 0.1
running = True
lock = threading.RLock()

def lurk():
    global old_process
    while running:
        time.sleep(check_every)
        with lock:
            if old_process and old_process.poll() is None:
                current_time = time.time()
                if current_time >= time_to_die:
                    logging.debug("lurk: killing old_process %s", old_process)
                    #old_process.communicate(input='q')
                    old_process.terminate()
                    old_process = None


def schedule_kill():
    global time_to_die
    time_started = time.time()
    time_to_die = time_started + start_delay

def play(videofile):
    global old_process, process
    with lock:
        if not old_process:
            logging.debug("no old_process")
        else:
            logging.debug("play: killing old_process %s", old_process)
            try:
                #old_process.communicate(input='q')
                old_process.terminate()
            except OSError:
                logging.debug("could not kill old_process, already dead?")
        old_process = process
        process = start_video(videofile)
        schedule_kill()

def is_stopped():
    with lock:
        return process and (process.poll() is not None)

def quit():
    global running
    running = False
    killer.join()
    with lock:
        process.wait()

killer = threading.Thread(target=lurk)
killer.start()

__all__ = ['play', 'quit', 'is_stopped', 'start_delay']
