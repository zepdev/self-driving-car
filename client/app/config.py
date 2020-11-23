import logging

# Redis
REDIS_HOST = "localhost"
REDIS_PORT = "6379"
DB_ID = "0"
QUEUE_NAME = "queue"
GAMEPAD = "gamepad"

# Logging
LOG_LEVEL = "INFO"
logging.basicConfig(format="%(asctime)s %(message)s", level=LOG_LEVEL)

# Pins
TRIGGER_1 = 21  # front
TRIGGER_2 = 22  # back-left
TRIGGER_3 = 20  # back-right
ECHO_1 = 24
ECHO_2 = 17
ECHO_3 = 18
TRIGGERS = []  # TRIGGER_1, TRIGGER_2, TRIGGER_3
ECHOS = []  # ECHO_1, ECHO_2, ECHO_3
SERVO_PIN = 12

# Motor (Should not change the PIN numbers, this is specific for the motor driver head.)
MAX_SPEED = 40  # Percentage of maximal possible speed (before: 150/480=0.3125)
PWM_PIN = 13
EN_PIN = 23
DIR_PIN = 25
FLT_PIN = 6

# Servo angles
servo_angles = {
    "SERVO_MIN_ANGLE": 4.5,
    "SERVO_MIDDLE_ANGLE": 7,
    "SERVO_MAX_ANGLE": 9.5
}

# Others
START_SLEEP_TIME = 30  # Sleep long on auto-start to give docker-compose time to start
RECORD_SLEEP_TIME = 0.6
MAIN_SLEEP_TIME = 1

# model
model_path = "models/nils_model_converted.tflite"

