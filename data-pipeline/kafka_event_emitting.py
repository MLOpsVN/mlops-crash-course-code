from kafka.admin import KafkaAdminClient, NewTopic
from kafka.producer import KafkaProducer
import argparse
import json
import pandas as pd
from time import sleep

from constants import logger

def main(args):
    print(args.bootstrap_servers)
    # initialize admin and producer
    admin = KafkaAdminClient(
        bootstrap_servers=[args.bootstrap_servers], 
        client_id="driver_stats_admin"
    )

    producer = KafkaProducer(
        bootstrap_servers=[args.bootstrap_servers], 
        client_id="driver_stats_producer"
    )
        
    # create Kafka topic
    topic_name = "driver_stats_topic"
    topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
    admin.create_topics(new_topics=[topic])

    # publish messages to the newly created topic
    df = pd.read_parquet("data/driver_stats_stream.parquet").sort_values(by="event_timestamp")
    records = df[["driver_id", "event_timestamp", "created", "conv_rate", "acc_rate"]].to_dict("records")

    iteration = 1
    while True:
        for record in records:
            record["event_timestamp"] = (
                record["event_timestamp"] + pd.Timedelta(weeks=52 * iteration)
            ).strftime("%Y-%m-%d %H:%M:%S")
            record["created"] = record["created"].strftime("%Y-%m-%d %H:%M:%S")
            producer.send(topic_name, json.dumps(record).encode())
            sleep(1.0)
            logger.info(record)
        iteration += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Kafka event emiting.')
    parser.add_argument('-b', '--bootstrap_servers', default="127.0.0.1:9092",
                        help='Kafka bootstrap servers')

    args = parser.parse_args()
    main(args)