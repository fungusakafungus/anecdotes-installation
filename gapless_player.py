import os
import subprocess
import threading
import time

#MY_PATH = os.path.dirname(__file__)
#PLAYER = MY_PATH + "/omxplayer-simple"
PLAYER = './omxplayer-simple'

def start_video(filename):
    return subprocess.Popen([PLAYER, filename], stdin=subprocess.PIPE)

class GaplessPlayer(object):
    old_process = None
    process = None
    start_delay = 2.7
    check_every = 0.1
    running = True
    lock = threading.RLock()

    @classmethod
    def lurk(cls):
        while cls.running:
            time.sleep(cls.check_every)
            with cls.lock:
                if cls.old_process and cls.old_process.poll != None:
                    current_time = time.time()
                    if current_time >= cls.time_to_die:
                        cls.old_process.kill()
                        cls.old_process = None


    @classmethod
    def schedule_kill(cls):
        time_started = time.time()
        cls.time_to_die = time_started + cls.start_delay

    @classmethod
    def play(cls, videofile):
        with cls.lock:
            cls.old_process = cls.process
            cls.process = start_video(videofile)
            cls.schedule_kill()

    @classmethod
    def is_stopped(cls):
        return cls.process and (cls.process.poll() is not None)

    @classmethod
    def quit(cls):
        cls.running = False
        killer.join()

killer = threading.Thread(target=GaplessPlayer.lurk)
killer.start()
