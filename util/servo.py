import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# GPIO 4
GPIO.setup(4, GPIO.OUT)

# GPIO4 PWM, 周波数:50Hz
p = GPIO.PWM(4, 50)


def set_servo(degree):
    dc = 2.5 + (12.0 - 2.5) / 180 * (degree + 90)
    p.ChangeDutyCycle(dc)
