from ConfigParser import ConfigParser
import logging
import collections
import os

logger = logging.getLogger("button")
MY_PATH = os.path.dirname(__file__) or os.getcwd()


def read_config():
    config = ConfigParser()
    config.readfp(open(MY_PATH + '/config-default.ini'))
    config.read(MY_PATH + "/config.ini")
    window_size_seconds = config.getfloat(
        "anecdotes",
        "button_press_seconds"
    )
    logger.info(
        'button_press_seconds is configured to %s seconds',
        window_size_seconds
    )
    window_size = int(2 / 0.1 * window_size_seconds)
    logger.info(
        'button window size is %s',
        window_size
    )
    return window_size

window_size = read_config()
recent_states = collections.deque(maxlen=window_size)

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN)
except ImportError:
    GPIO = None
    print 'not running on a pi'


def hardware_get():
    if GPIO:
        return GPIO.input(17)

got_initial_state = False
activated = False
initial_state = None


def active():
    global got_initial_state, initial_state, activated
    if len(recent_states) == window_size:
        if not got_initial_state:
            initial_state = state()
            got_initial_state = True
        else:
            if initial_state == state():
                pass
            else:
                activated = True
                logger.info('activated button')


def state():
    l = sorted(list(recent_states))
    index = int(len(l) / 2)
    state = l[index]
    return state


def check():
    recent_states.append(hardware_get())
