import json
import uuid
import time
import redis
import boto3
import config
import base64
import logging
import datetime
from io import StringIO
import pandas as pd

redis_server = redis.StrictRedis(
    host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_ID
)


def dataframe_to_csv_on_s3(dataframe, filename):
    """ Write a dataframe to a CSV on S3 """

    csv_buffer = StringIO()
    dataframe.to_csv(csv_buffer, sep=",", index=True, header=True)

    s3_resource = boto3.resource("s3")
    s3_resource.Object(config.S3_BUCKET, filename).put(Body=csv_buffer.getvalue())


def picture_to_s3(pic, filename):
    s3_resource = boto3.resource("s3")
    s3_resource.Bucket(config.S3_BUCKET).put_object(Key=filename, Body=pic, ContentType='image/jpg') #ACL='public-read')


def datetime_to_iso(time):
    # time = datetime.datetime.now()
    iso = time.isoformat(sep="/")
    iso = iso.split(".")[0]
    iso = '-'.join(iso.split(':'))
    return iso


if __name__ == "__main__":

    logging.info("process_queue.py started.")
    logging.debug("Warning: Debugging is enabled.")

    while True:
        queue = redis_server.lrange(config.INPUT_QUEUE, 0, config.BATCH_SIZE - 1)
        batch = None

        if queue:
            logging.debug(f"Got {len(queue)} items from {config.INPUT_QUEUE}.")
            data = []
            index = []
            for q in queue:
                q = json.loads(q.decode("utf-8"))

                # distances and output
                d = q['dist'].copy()
                d.update(q['out'])
                data.append(d)

                # timestamp
                index.append(q['ts'])

                # picture
                pic_binary = q['pic'].encode("utf-8")
                img = base64.b64decode(pic_binary)

                # send it to S3
                try:
                    picture_to_s3(img,  f"{config.S3_DESTINATION}images/{q['ts']}.jpg")
                    logging.debug(f"{config.S3_DESTINATION}images/{q['ts']}.jpg")
                except Exception as e:
                    logging.exception(e)
                    continue

            if len(data) > 0:
                # Create data frame
                df = pd.DataFrame(data, index=index)

                # Define name for saving
                iso_dt = datetime_to_iso(datetime.datetime.now())
                filename = f"{config.S3_DESTINATION}data/{iso_dt}.csv"

                # Send data frame to S3
                try:
                    dataframe_to_csv_on_s3(df, filename)
                    logging.debug(filename)
                    logging.debug(df)
                except Exception as e:
                    logging.exception(e)
                    continue

            redis_server.ltrim(config.INPUT_QUEUE, len(queue), -1)
            logging.debug(f"Removed {len(queue)} items from {config.INPUT_QUEUE}.")

        time.sleep(config.PROCESS_SLEEP)
