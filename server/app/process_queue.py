import json
import uuid
import config
import time
import redis
import boto3
import datetime
from io import StringIO
import numpy as np
import pandas as pd

redis_server = redis.StrictRedis(
    host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_ID
)


def dataframe_to_csv_on_s3(dataframe, filename):
    """ Write a dataframe to a CSV on S3 """

    csv_buffer = StringIO()
    dataframe.to_csv(csv_buffer, sep=",", index=False, header=False)

    s3_resource = boto3.resource("s3")
    s3_resource.Object(config.S3_BUCKET, filename).put(Body=csv_buffer.getvalue())


if __name__ == "__main__":

    while True:
        queue = redis_server.lrange(config.INPUT_QUEUE, 0, config.BATCH_SIZE - 1)
        batch = None

        if queue:
            for q in queue:
                q = json.loads(q.decode("utf-8"))
                data = q["data"]

                if batch is None:
                    batch = np.array(data)
                else:
                    batch = np.vstack([batch, data])

            if batch.shape[0] > 0:
                df = pd.DataFrame(batch)

                iso_dt = datetime.datetime.now().isoformat(sep="/")
                iso_dt = iso_dt.split(".")[0]
                iso_dt = '-'.join(iso_dt.split(':'))
                hash_str = str(uuid.uuid4()).split('-')[0]
                filename = f"{config.S3_DESTINATION}{iso_dt}-{hash_str}.csv"

                try:
                    # dataframe_to_csv_on_s3(df, filename)
                    print(df, filename)
                except Exception as e:
                    print(e)
                    continue

                redis_server.ltrim(config.INPUT_QUEUE, df.shape[0], -1)

        time.sleep(config.PROCESS_SLEEP)