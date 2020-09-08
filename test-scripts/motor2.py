import Jetson.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
time.sleep(0.5)
en_pin = 23
GPIO.setup(en_pin, GPIO.OUT)
GPIO.output(en_pin, GPIO.HIGH)
dir_pin = 25
GPIO.setup(dir_pin, GPIO.OUT)
GPIO.output(dir_pin, GPIO.LOW)
pwm_pin = 13
GPIO.setup(pwm_pin, GPIO.OUT, initial=GPIO.HIGH)
p = GPIO.PWM(pwm_pin, 20000)
time.sleep(0.5)
p.start(20)
time.sleep(10)
