import RPi.GPIO as GPIO


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
        self.pwm.ChangeDutyCycle(speed)

    def enable(self):
        GPIO.output(self.en_pin, GPIO.HIGH)

    def disable(self):
        GPIO.output(self.en_pin, GPIO.LOW)


class Drive():
    
    def __init__(self, servo_pin, servo_angles, motor):
        self.MOTOR_FACTOR = 25  # Value between 0 and 100. 100 = use full available power of motor
        
        self.SERVO_MIN_ANGLE = servo_angles["SERVO_MIN_ANGLE"]
        self.SERVO_MIDDLE_ANGLE = servo_angles["SERVO_MIDDLE_ANGLE"]
        self.SERVO_MAX_ANGLE = servo_angles["SERVO_MAX_ANGLE"]
        
        self.servo = GPIO.PWM(servo_pin, 50)
        self.servo.start(self.SERVO_MIDDLE_ANGLE)

        self.motor = motor
        self.motor.enable()
        # self.motor.setSpeed(0)
    
    def _steer(self, x):
        """
        :param x: float between -1 and 1
        """
        angle = self.SERVO_MIN_ANGLE + (x + 1)*(self.SERVO_MAX_ANGLE-self.SERVO_MIN_ANGLE) / 2
        return angle
    
    def disable(self):
        self.motor.setSpeed(0)
        self.motor.disable()
        self.servo.stop()
    
    def drive(self, output_dict):
        self.motor.setSpeed((-round((output_dict["ABS_Y"]+0.5)/32767.5, 1))*self.MOTOR_FACTOR)
        servo_angle = self._steer(-round((output_dict["ABS_RX"]+0.5)/32767.5, 1)) 
        self.servo.ChangeDutyCycle(servo_angle)
