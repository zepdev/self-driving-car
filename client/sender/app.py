import sys
import time
import json
import redis
import config
import logging
from connector import APIConnector

# Setup redis
db = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.DB_ID)

# Create an instance of APIConnector
sender = APIConnector(msg_broker_base_url=config.MSG_BROKER_BASE_URL, user=config.USER, pwd=config.PASSWORD)

# Authenticate the first time
token = sender.auth_client()
data = []

logging.info("Successfully authenticated and connected to server on AWS. App started.")
logging.debug("Warning: Debugging is enabled.")
time.sleep(config.SLEEP_TIME)

while True:

    # Check if there is something in the queue. If so, get all objects.
    data = db.lrange(config.QUEUE_NAME, 0, -1)
    data = [json.loads(item) for item in data]

    if len(data) > 0:

        # Send data to server
        status = sender.post_data(data, token)

        if status == 200:
            # Remove all items that were sent to the server
            logging.info(f"Sent {len(data)} objects to server.")
            db.ltrim(config.QUEUE_NAME, len(data), -1)
        elif status == 401:
            # Authentication expired, authenticate again
            token = sender.auth_client()
            logging.debug("Authentication was expired. New authentication was successful.")
            continue  # in this case, do not sleep
        else:
            # Something failed, do not remove data from queue
            logging.error(f"Could not send {len(data)} objects to server. Trying again.")

    time.sleep(config.SLEEP_TIME)