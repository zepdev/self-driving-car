import RPi.GPIO as GPIO
from dual_g2_hpmd_rpi import motors  # TODO: write this by myself, see below


class Motor():

    def __init__(self):
        # this is from the dual_g2_hpmd_rpi library
        self.pwm_pin = 13
        self.dir_pin = 25
        self.en_pin = 23
        self.flt_pin = 6

        self.MAX_SPEED = 480

        # TODO: Translate the following to GPIO: https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
        # (from pigpio: http://abyz.me.uk/rpi/pigpio/python.html)

        #_pi.set_pull_up_down(flt_pin, pigpio.PUD_UP)  # make sure FLT is pulled up
        #_pi.write(en_pin, 1)  # enable driver by default

    def setSpeed(self, speed):
        if speed < 0:
            speed = -speed
            dir_value = 1
        else:
            dir_value = 0

        if speed > self.MAX_SPEED:
            speed = self.MAX_SPEED

        # TODO: translate this
        #_pi.write(self.dir_pin, dir_value)
        #_pi.hardware_PWM(self.pwm_pin, 20000, int(speed * 6250 / 3));
          # 20 kHz PWM, duty cycle in range 0-1000000 as expected by pigpio

    def enable(self):
        # TODO: translate this
        #_pi.write(self.en_pin, 1)

    def disable(self):
        # TODO: translate this
        #_pi.write(self.en_pin, 0)


# TODO: instantiate motor from Motor (maybe give the pins?) and change code below accordingly

class Drive():
    
    def __init__(self, servo_pin, servo_angles):
        self.MOTOR_FACTOR = 150
        
        self.SERVO_MIN_ANGLE = servo_angles["SERVO_MIN_ANGLE"]
        self.SERVO_MIDDLE_ANGLE = servo_angles["SERVO_MIDDLE_ANGLE"]
        self.SERVO_MAX_ANGLE = servo_angles["SERVO_MAX_ANGLE"]
        
        self.servo = GPIO.PWM(servo_pin, 50)
        self.servo.start(self.SERVO_MIDDLE_ANGLE)
        
        motors.enable()
        self.motor = motors.motor2
        self.motor.setSpeed(0)
    
    def _steer(self, x):
        """
        :param x: float between -1 and 1
        """
        angle = self.SERVO_MIN_ANGLE + (x + 1)*(self.SERVO_MAX_ANGLE-self.SERVO_MIN_ANGLE) / 2
        return angle
    
    def disable(self):
        self.motor.setSpeed(0)
        motors.disable()
        self.servo.stop()
    
    def drive(self, output_dict):
        self.motor.setSpeed((-round((output_dict["ABS_Y"]+0.5)/32767.5, 1))*self.MOTOR_FACTOR)
        servo_angle = self._steer(-round((output_dict["ABS_RX"]+0.5)/32767.5, 1)) 
        self.servo.ChangeDutyCycle(servo_angle)
