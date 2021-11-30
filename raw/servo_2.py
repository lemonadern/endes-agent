import time

# GPIOの初期設定
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# GPIO 4
GPIO.setup(4, GPIO.OUT)

# GPIO4 PWM, 周波数:50Hz
p = GPIO.PWM(4, 50)

# Duty Cycle 0%
p.start(0.0)

while True:
    print("input degree")
    degree = float(input())

    dc = 2.5 + (12.0 - 2.5) / 180 * (degree + 90)

    # DutyCycle dc%
    p.ChangeDutyCycle(dc)

    # 最大180°回転を想定し、0.3sec以上待つ
    time.sleep(0.4)

    # 回転終了したら一旦 DutyCycle を 0% に戻す
    p.ChangeDutyCycle(0.0)
