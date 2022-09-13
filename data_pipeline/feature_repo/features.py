from datetime import timedelta

from feast import FeatureView, Field
from feast.stream_feature_view import stream_feature_view
from feast.types import Float32, Int32
from pyspark.sql import DataFrame

from data_sources import driver_stats_batch_source, driver_stats_stream_source
from entities import driver

driver_stats_view = FeatureView(
    name="driver_stats",
    description="driver features",
    entities=[driver],
    ttl=timedelta(days=36500),
    schema=[
        Field(name="conv_rate", dtype=Float32),
        Field(name="acc_rate", dtype=Float32),
        Field(name="avg_daily_trips", dtype=Int32),
    ],
    online=True,
    source=driver_stats_batch_source,
    tags={},
    owner="mlopsvn@gmail.com",
)


@stream_feature_view(
    entities=[driver],
    ttl=timedelta(days=36500),
    mode="spark",
    schema=[
        Field(name="conv_rate", dtype=Float32),
        Field(name="acc_rate", dtype=Float32),
    ],
    timestamp_field="datetime",
    online=True,
    source=driver_stats_stream_source,
    tags={},
    owner="stream_source_owner@gmail.com",
)
def driver_stats_stream(df: DataFrame):
    from pyspark.sql.functions import col

    return (
        df.withColumn("conv_percentage", col("conv_rate") * 100.0)
        .withColumn("acc_percentage", col("acc_rate") * 100.0)
        .drop("conv_rate", "acc_rate")
        .withColumnRenamed("conv_percentage", "conv_rate")
        .withColumnRenamed("acc_percentage", "acc_rate")
    )
