import os
from datetime import timedelta
from pathlib import Path

from feast import FileSource, KafkaSource
from feast.data_format import JsonFormat, ParquetFormat

FEATURE_STORE_DIR_ENV_VAR_NAME = "FEATURE_STORE_DIR"
feature_store_dir = os.environ.get(FEATURE_STORE_DIR_ENV_VAR_NAME, "")
if feature_store_dir == "":
    raise Exception(f"Env var {FEATURE_STORE_DIR_ENV_VAR_NAME} is not set")

feature_store_dir = Path(feature_store_dir)
driver_stats_parquet_file = feature_store_dir / "data_sources/driver_stats.parquet"

driver_stats_batch_source = FileSource(
    name="driver_stats",
    file_format=ParquetFormat(),
    path=driver_stats_parquet_file.absolute().as_posix(),
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
