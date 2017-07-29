import RPi.GPIO as GPIO
from time import sleep
import requests
import json

GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor1B = 18
Motor1E = 22

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

lastState = ""

while True:
    state = json.loads(requests.get("https://build-box-test.herokuapp.com/state").content)['state']

    if lastState != state:
        lastState = state

        print "Turning motor on"
        GPIO.output(Motor1A, GPIO.HIGH)
        GPIO.output(Motor1B, GPIO.LOW)
        GPIO.output(Motor1E, GPIO.HIGH)

        sleep(1)

        print "Going backwards"
        GPIO.output(Motor1A, GPIO.LOW)
        GPIO.output(Motor1B, GPIO.HIGH)
        GPIO.output(Motor1E, GPIO.HIGH)

        sleep(.5)

        print "Stopping motor"
        GPIO.output(Motor1E, GPIO.LOW)
        sleep(.001)

GPIO.output(Motor1E, GPIO.LOW)

GPIO.cleanup()
