import os
import subprocess
import threading
import time

#MY_PATH = os.path.dirname(__file__)
#PLAYER = MY_PATH + "/omxplayer-simple"
PLAYER = './omxplayer-simple'

def start_video(filename):
    return subprocess.Popen([PLAYER, filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

old_process = None
process = None
start_delay = 2.7
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
                    old_process.kill()
                    old_process = None


def schedule_kill():
    global time_to_die
    time_started = time.time()
    time_to_die = time_started + start_delay

def play(videofile):
    global old_process, process
    with lock:
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
