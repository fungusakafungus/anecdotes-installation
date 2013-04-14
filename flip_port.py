import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 23
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)

if GPIO.input(GPIO_TRIGGER):
	print False
	GPIO.output(GPIO_TRIGGER, False)
else:
	print True
	GPIO.output(GPIO_TRIGGER, True)
