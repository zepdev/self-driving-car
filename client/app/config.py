import logging
import RPi.GPIO as GPIO

# Redis
REDIS_HOST = "localhost"
REDIS_PORT = "6379"
DB_ID = "0"
QUEUE_NAME = "queue"
CHANNEL_GAMEPAD = "gamepad"

# Logging
LOG_LEVEL = "DEBUG"
logging.basicConfig(format="%(asctime)s %(message)s", level=LOG_LEVEL)

# Pins
TRIGGER_1 = 21
#TRIGGER_2
#TRIGGER_3
ECHO_1 = 24
#ECH0_2
#ECHO_3
TRIGGERS = [TRIGGER_1]  # , TRIGGER_2, TRIGGER_3]
ECHOS = [ECHO_1]
SERVO_PIN = 18

# Others
RECORD_SLEEP_TIME = 0.3


