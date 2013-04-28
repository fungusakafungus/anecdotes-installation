import sys
try:
    import RPi.GPIO as GPIO
    import ultrasonic
    GPIO.setwarnings(False)

except ImportError:
    GPIO = None
    import getch
    print "looks like we are not running on a raspberry pi!"

OUTGOING = False
INCOMING = True
MIN_DISTANCE = 20
MAX_DISTANCE = 80

last_state = OUTGOING

def state():
    global last_state
    if GPIO:
        distance = ultrasonic.distance()
        if not distance:
            return last_state
        sys.stdout.write("\r%d" % int(distance))
        sys.stdout.flush()
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
