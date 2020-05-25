import os
import logging

# Redis
REDIS_HOST = "localhost"
REDIS_PORT = "6379"
DB_ID = "0"
QUEUE_NAME = "queue"

# Logging
LOG_LEVEL = "DEBUG"
logging.basicConfig(format="%(asctime)s %(message)s", level=LOG_LEVEL)