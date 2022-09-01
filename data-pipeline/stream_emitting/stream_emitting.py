from kafka.admin import KafkaAdminClient, NewTopic
from kafka.producer import KafkaProducer
import argparse
import json
import pandas as pd
from time import sleep

from utils import logger

def main(args):
    # initialize admin and producer
    admin = KafkaAdminClient(
        bootstrap_servers=[args.bootstrap_servers], 
        client_id="driver_stats_admin"
    )

    producer = KafkaProducer(
        bootstrap_servers=[args.bootstrap_servers], 
        client_id="driver_stats_producer"
    )
        
    # create a Kafka topic
    topic = NewTopic(name=args.topic_name, num_partitions=1, replication_factor=1)
    admin.create_topics(new_topics=[topic])

    # publish messages to the newly created topic
    df = pd.read_parquet(args.data).sort_values(by="event_timestamp")
    records = df[["driver_id", "event_timestamp", "created", "conv_rate", "acc_rate"]].to_dict("records")

    # simulate streaming events by increase one week for every records
    iteration = 1
    while True:
        for record in records:
            record["event_timestamp"] = (
                record["event_timestamp"] + pd.Timedelta(weeks=iteration)
            ).strftime("%Y-%m-%d %H:%M:%S")
            record["created"] = record["created"].strftime("%Y-%m-%d %H:%M:%S")
            producer.send(args.topic_name, json.dumps(record).encode())
            # sleep 5 seconds before continuing pushing events 
            sleep(5)
            logger.info(record)
        iteration += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Kafka event emiting.')
    parser.add_argument('-b', '--bootstrap_servers', default="127.0.0.1:9092",
                        help='Kafka bootstrap servers')
    parser.add_argument('-t', '--topic_name', default="drivers",
                        help='Kafka topic name')
    parser.add_argument('-d', '--data', default="data/driver_stats_stream.parquet",
                        help='data path to create streams')
    args = parser.parse_args()
    main(args)