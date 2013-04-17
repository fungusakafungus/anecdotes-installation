try:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)

    GPIO.setmode(GPIO.BCM)
    GPIO_TRIGGER = 23
    GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
except ImportError:
    GPIO = None
    print "looks like we are not running on a raspberry pi!"

def state():
    if GPIO:
        return GPIO.input(GPIO_TRIGGER)
    else:
        return False