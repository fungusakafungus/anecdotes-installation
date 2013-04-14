import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 23
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)

def state():
    return GPIO.input(GPIO_TRIGGER)
