from datetime import timedelta

from feast import FileSource, KafkaSource
from feast.data_format import JsonFormat, ParquetFormat

driver_stats_parquet_file = "../data_sources/driver_stats.parquet"

driver_stats_batch_source = FileSource(
    name="driver_stats",
    file_format=ParquetFormat(),
    path=driver_stats_parquet_file,
    timestamp_field="datetime",
    created_timestamp_column="created",
)

driver_stats_stream_source = KafkaSource(
    name="driver_stats_stream",
    kafka_bootstrap_servers="localhost:29092",
    topic="drivers",
    timestamp_field="datetime",
    batch_source=driver_stats_batch_source,
    message_format=JsonFormat(
        schema_json="driver_id integer, acc_rate double, conv_rate double, datetime timestamp, created timestamp"
    ),
    watermark_delay_threshold=timedelta(minutes=5),
    description="The Kafka stream containing the driver stats",
)
