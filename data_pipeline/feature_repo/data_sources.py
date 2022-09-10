from datetime import timedelta

from feast import (
    KafkaSource,
    FileSource,
)

from feast.data_format import JsonFormat, ParquetFormat


driver_stats_batch_source = FileSource(
    name="driver_stats",
    file_format=ParquetFormat(),
    path="../data/driver_stats.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
)

driver_stats_stream_source = KafkaSource(
    name="driver_stats_stream",
    kafka_bootstrap_servers="localhost:29092",
    topic="drivers", 
    timestamp_field="event_timestamp",
    batch_source=driver_stats_batch_source,
    message_format=JsonFormat(
        schema_json="driver_id integer, acc_rate double, conv_rate double, event_timestamp timestamp, created timestamp"
    ),
    watermark_delay_threshold=timedelta(minutes=5),
    description="The Kafka stream containing the driver stats",
)
