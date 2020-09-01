from __future__ import print_function
import time
from dual_g2_hpmd_rpi import motors

MAX_SPEED = 120
# Set up sequences of motor speeds.
test_forward_speeds = list(range(40, MAX_SPEED, 1)) + \
  list(range(MAX_SPEED, 40, -1)) + [40]  

test_reverse_speeds = list(range(-40, -MAX_SPEED, -1)) + \
  list(range(-MAX_SPEED, -40, 1)) + [-40]  

try:
    motors.enable()
    motors.setSpeeds(0, 0)

    print("Motor 2 forward")
    for s in test_forward_speeds:
        print(s)
        motors.motor2.setSpeed(s)
        time.sleep(0.2)

    print("Motor 2 reverse")
    for s in test_reverse_speeds:
        print(s)
        motors.motor2.setSpeed(s)
        time.sleep(0.2)

finally:
  # Stop the motors, even if there is an exception
  # or the user presses Ctrl+C to kill the process.
  motors.setSpeeds(0, 0)
  motors.disable()
