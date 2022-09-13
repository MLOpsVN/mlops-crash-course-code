from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
import argparse
import json
import pandas as pd
from time import sleep

import logging
import sys

# logging initialization
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

def main(args):
    for _ in range(20):
        try:
            # initialize admin and producer
            producer = KafkaProducer(
                bootstrap_servers=[args.bootstrap_servers], 
                client_id="driver_stats_producer",
            )

            admin = KafkaAdminClient(
                bootstrap_servers=[args.bootstrap_servers],
                client_id="driver_stats_admin",
            )

            logger.info("Starting admin and producer successfully!")
            break
        except Exception as e:
            logger.info(f"Failed to start admin and producer with error {e}")
            sleep(20)
            pass
    
    try:
        # create a Kafka topic
        topic = NewTopic(name=args.topic_name, num_partitions=1, replication_factor=1)
        admin.create_topics(new_topics=[topic])
        logger.info(f"Created topic {args.topic_name}")
    except Exception as e:
        logger.info(f"Failed to create a new topic with error {e}")
        sleep(20)
        pass

    # publish messages to the newly created topic
    df = pd.read_parquet(args.data).sort_values(by="datetime")
    records = df[["driver_id", "datetime", "created", "conv_rate", "acc_rate"]].to_dict("records")

    # simulate streaming events by increase one week for every records
    iteration = 1
    while True:
        for record in records:
            record["datetime"] = (
                record["datetime"] + pd.Timedelta(weeks=iteration)
            ).strftime("%Y-%m-%d %H:%M:%S")
            record["created"] = record["created"].strftime("%Y-%m-%d %H:%M:%S")
            producer.send(args.topic_name, json.dumps(record).encode())
            # sleep 5 seconds before continuing pushing events 
            sleep(5)
            logger.info(record)
        iteration += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Kafka event emiting.')
    parser.add_argument('-b', '--bootstrap_servers', default="localhost:29092",
                        help='Kafka bootstrap servers')
    parser.add_argument('-t', '--topic_name', default="drivers",
                        help='Kafka topic name')
    parser.add_argument('-d', '--data', default="data/driver_stats_stream.parquet",
                        help='data path to create streams')
    args = parser.parse_args()
    main(args)