import logging

# Redis
REDIS_HOST = "localhost"
REDIS_PORT = "6379"
DB_ID = "0"
QUEUE_NAME = "queue"
GAMEPAD = "gamepad"

# Logging
LOG_LEVEL = "DEBUG"
logging.basicConfig(format="%(asctime)s %(message)s", level=LOG_LEVEL)

# Pins
TRIGGER_1 = 21 #front
#TRIGGER_2 = 22 
#TRIGGER_3 = 22
ECHO_1 = 24
#ECHO_2 = 25
#ECHO_3 = 25
TRIGGERS = [TRIGGER_1]#, TRIGGER_2]#, TRIGGER_3]
ECHOS = [ECHO_1]#, ECHO_2]#, ECHO_3]
SERVO_PIN = 18

# Servo angles
servo_angles = {
    "SERVO_MIN_ANGLE": 4.5,
    "SERVO_MIDDLE_ANGLE": 7,
    "SERVO_MAX_ANGLE": 9.5
}

# Others
RECORD_SLEEP_TIME = 0.6
MAIN_SLEEP_TIME = 1


