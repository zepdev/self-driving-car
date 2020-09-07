import time
import RPi.GPIO as GPIO

MAX_SPEED = 100
# Set up sequences of motor speeds.
test_forward_speeds = list(range(40, MAX_SPEED, 1)) + \
  list(range(MAX_SPEED, 40, -1)) + [40]  

test_reverse_speeds = list(range(-40, -MAX_SPEED, -1)) + \
  list(range(-MAX_SPEED, -40, 1)) + [-40]  





# from dual_g2_hpmd_rpi import motors
GPIO.setmode(GPIO.BCM)

class Motor():

    def __init__(self):

        self.dir_pin = 25  # controls direction (forward/backward)
        GPIO.setup(self.dir_pin, GPIO.OUT)

        self.flt_pin = 6  # pin for faults, could write a function get-fault, see dual_g2_hpmd_rpi
        GPIO.setup(self.flt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # make sure FLT is pulled up

        self.en_pin = 23  # enables/ disables motor
        GPIO.setup(self.en_pin, GPIO.OUT)
        GPIO.output(self.en_pin, GPIO.HIGH) # enable driver by default
        
        self.MAX_SPEED = 100

	# this is from the dual_g2_hpmd_rpi library
        self.pwm_pin = 13
        self.pwm = GPIO.PWM(self.pwm_pin, 20000)  # set frequency
        self.pwm.start(0)  # duty-cycle=0 -> speed=0

    def setSpeed(self, speed):
        if speed < 0:
            speed = -speed
            dir_value = 1  # backward
        else:
            dir_value = 0  # forward

        if speed > self.MAX_SPEED:
            speed = self.MAX_SPEED

        GPIO.output(self.dir_pin, dir_value)

        GPIO.setup(self.pwm_pin, GPIO.OUT)
        self.pwm.ChangeDutyCycle(speed)

    def enable(self):
        GPIO.output(self.en_pin, GPIO.HIGH)

    def disable(self):
        GPIO.output(self.en_pin, GPIO.LOW)


motor = Motor()

try:
    motor.enable()
    motor.setSpeed(0)

    print("Motor 2 forward")
    for s in test_forward_speeds:
        print(s)
        motor.setSpeed(s)
        time.sleep(0.2)

    print("Motor 2 reverse")
    for s in test_reverse_speeds:
        print(s)
        motor.setSpeed(s)
        time.sleep(0.2)

finally:
  # Stop the motors, even if there is an exception
  # or the user presses Ctrl+C to kill the process.
  motor.setSpeed(0)
  motor.disable()
