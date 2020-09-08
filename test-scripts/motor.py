import time
import RPi.GPIO as GPIO

MAX_SPEED = 100
# Set up sequences of motor speeds.
test_forward_speeds = list(range(20, MAX_SPEED, 1)) + \
  list(range(MAX_SPEED, 20, -1)) + [20]  

test_reverse_speeds = list(range(-20, -MAX_SPEED, -1)) + \
  list(range(-MAX_SPEED, -20, 1)) + [-20]  

GPIO.setmode(GPIO.BCM)


class Motor():

    def __init__(self):

        self.MAX_SPEED = 100

        self.flt_pin = 6  # pin for faults, could write a function get-fault, see dual_g2_hpmd_rpi
        GPIO.setup(self.flt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # make sure FLT is pulled up

        self.en_pin = 23  # enables/ disables motor
        GPIO.setup(self.en_pin, GPIO.OUT)
        GPIO.output(self.en_pin, GPIO.HIGH) # enable driver by default
        
        self.dir_pin = 25  # controls direction (forward/backward)
        GPIO.setup(self.dir_pin, GPIO.OUT)
	
        self.pwm_pin = 13
        GPIO.setup(self.pwm_pin, GPIO.OUT, initial=GPIO.HIGH)
        self.pwm = GPIO.PWM(self.pwm_pin, 20000)  # set frequency
        self.pwm.start(0)  # duty-cycle=0 -> speed=0 (percent, 0 to 100)

    def setSpeed(self, speed):
        if speed < 0:
            speed = -speed
            dir_value = 1  # backward
        else:
            dir_value = 0  # forward

        if speed > self.MAX_SPEED:
            speed = self.MAX_SPEED

        GPIO.output(self.dir_pin, dir_value)
        self.pwm.ChangeDutyCycle(speed)

    def enable(self):
        GPIO.output(self.en_pin, GPIO.HIGH)

    def disable(self):
        GPIO.output(self.en_pin, GPIO.LOW)


motor = Motor()

try:
    motor.enable()
    motor.setSpeed(0)

    print("Motor forward")
    for s in test_forward_speeds:
        print(s)
        motor.setSpeed(s)
        time.sleep(1)

    print("Motor reverse")
    for s in test_reverse_speeds:
        print(s)
        motor.setSpeed(s)
        time.sleep(1)

finally:
  # Stop the motors, even if there is an exception
  # or the user presses Ctrl+C to kill the process.
  motor.setSpeed(0)
  motor.disable()
