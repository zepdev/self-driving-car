import time
import RPi.GPIO as GPIO
from dual_g2_hpmd_rpi import motors


class Drive():
	
	def __init__(self, servo_pin):
		self.FACTOR = 12
		
		self.SERVO_MIN_ANGLE = 5.5
		self.SERVO_MIDDLE_ANGLE = 7
		self.SERVO_MAX_ANGLE = 8.5
		
		self.servo = GPIO.PWM(servo_pin,50)
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
		self.motor.setSpeed((-round((output_dict["ABS_Y"]+0.5)/32767.5, 1))*self.FACTOR)
		
		servo_angle = self._steer(-round((output_dict["ABS_RX"]+0.5)/32767.5, 1)) 
		self.servo.ChangeDutyCycle(servo_angle)
		
	
	#bei drive koennten wir ein if statement einbauen, dass sich der Motor auch schon bei einem Input-Signal von 0.1 oder 0.2 dreht 
	#(Range: 40 bis 120 und -40 bis -120)
