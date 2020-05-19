import os
import logging

# Redis
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
DB_ID = os.environ["DB_ID"]
QUEUE_NAME = os.environ["QUEUE_NAME"]

# Logging
LOG_LEVEL = os.environ["LOG_LEVEL"]
logging.basicConfig(format="%(asctime)s %(message)s", level=LOG_LEVEL)