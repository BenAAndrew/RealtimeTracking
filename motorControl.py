import RPi.GPIO as GPIO
import time

REFRESH_RATE = 50
SLEEP_TIME = 0.15
MIN_VALUE = 2.5
MAX_VALUE = 12.5
RANGE = MAX_VALUE - MIN_VALUE


def connect_motor(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    p = GPIO.PWM(pin, REFRESH_RATE)
    p.start(MIN_VALUE)
    p.ChangeDutyCycle(MIN_VALUE)
    time.sleep(0.5)
    return p


def change_position(motor, position):
    if position >= MIN_VALUE and position <= MAX_VALUE:
        motor.ChangeDutyCycle(position)
        time.sleep(SLEEP_TIME)
    else:
        print(f"{position} outside range")

motor = connect_motor(17)
change_position(motor, 12.5)
motor.stop()
GPIO.cleanup()
