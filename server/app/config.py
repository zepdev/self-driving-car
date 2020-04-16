import os
import logging

# get variables from environment
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
REDIS_ID = os.environ["REDIS_ID"]
INPUT_QUEUE = os.environ["INPUT_QUEUE"]
BATCH_SIZE = int(os.environ["BATCH_SIZE"])
PROCESS_SLEEP = int(os.environ["PROCESS_SLEEP_MIN"]) * 60
S3_BUCKET = os.environ["S3_BUCKET"]
S3_DESTINATION = os.environ["S3_DESTINATION"]
LOG_LEVEL = os.environ["LOG_LEVEL"]

# logging
logging.basicConfig(format="%(asctime)s %(message)s", level=LOG_LEVEL)