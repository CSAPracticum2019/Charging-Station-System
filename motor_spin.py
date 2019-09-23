import RPi.GPIO as GPIO
import time


def open():
    GPIO.setmode(GPIO.BOARD)

    ControlPin = [13, 15, 7, 11]

    for pin in ControlPin:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    seq = [[1, 0, 0, 1],
           [0, 0, 1, 1],
           [0, 0, 1, 0],
           [0, 1, 1, 0],
           [0, 1, 0, 0],
           [1, 1, 0, 0],
           [1, 0, 0, 0],
           [1, 0, 0, 0]]

    for i in range(75):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(ControlPin[pin], seq[halfstep][pin])
            time.sleep(.001)

    GPIO.cleanup()


def close():
    GPIO.setmode(GPIO.BOARD)

    ControlPin = [13, 15, 7, 11]

    for pin in ControlPin:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    seq = [[1, 0, 0, 0],
           [1, 1, 0, 0],
           [0, 1, 0, 0],
           [0, 1, 1, 0],
           [0, 0, 1, 0],
           [0, 0, 1, 1],
           [0, 0, 0, 1],
           [1, 0, 0, 1]]

    for i in range(75):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(ControlPin[pin], seq[halfstep][pin])
            time.sleep(.001)

    GPIO.cleanup()

