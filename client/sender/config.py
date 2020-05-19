import os
import logging

# Redis
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
DB_ID = os.environ["DB_ID"]
QUEUE_NAME = os.environ["QUEUE_NAME"]

# AWS
MSG_BROKER_BASE_URL = os.environ["MSG_BROKER_BASE_URL"]
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]

# Others
SLEEP_TIME = int(os.environ["SENDER_INTERVAL_SEC"])

# Logging
LOG_LEVEL = os.environ["LOG_LEVEL"]
logging.basicConfig(format="%(asctime)s %(message)s", level=LOG_LEVEL)