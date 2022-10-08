import argparse
from datetime import datetime, timedelta

import flask
import pandas as pd
import prometheus_client
from evidently.model_monitoring import (
    ClassificationPerformanceMonitor,
    DataDriftMonitor,
    ModelMonitoring,
)
from evidently.pipeline.column_mapping import ColumnMapping
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from utils import *

Log(AppConst.MONITORING_SERVICE)
AppPath()
app = Flask(AppConst.MONITORING_SERVICE)

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(
    app.wsgi_app, {"/metrics": prometheus_client.make_wsgi_app()}
)
pd.set_option("display.max_columns", None)


def read_reference_data() -> pd.DataFrame:
    Log().log.info("read_reference_data")
    reference_data = pd.read_parquet(AppPath.REFERENCE_PQ, engine="fastparquet")
    return reference_data


def read_label_data() -> pd.DataFrame:
    Log().log.info("read_label_data")
    label_file = AppPath.REQUEST_DATA
    if not label_file.exists():
        return None

    label_data = pd.read_csv(label_file)
    return label_data


def merge_request_with_label(
    new_rows: pd.DataFrame, label_data: pd.DataFrame
) -> pd.DataFrame:
    Log().log.info("_merge_request_with_label")
    merged_data = pd.merge(
        left=new_rows, right=label_data, how="inner", on="request_id"
    )
    merged_data["prediction"] = 1
    return merged_data


class MonitoringService:
    DATASET_NAME = "drivers"
    WINDOW_SIZE = 5
    RUN_PERIOD_SEC = 5
    DATETIME_COL = "datetime"
    NUMERICAL_COLS = ["conv_rate", "acc_rate", "avg_daily_trips"]
    CATEGORICAL_COLS = []
    TARGET_COL = "trip_completed"
    PREDICTION_COL = "prediction"

    def __init__(self) -> None:
        self.next_run = None
        self.current_data = None
        self.metrics = {}

        # read reference data
        self.reference_data = read_reference_data()
        Log().log.info(f"reference_data {self.reference_data}")

        # init column mapping
        self.column_mapping = ColumnMapping(
            target=self.TARGET_COL,
            prediction=self.PREDICTION_COL,
            numerical_features=self.NUMERICAL_COLS,
            categorical_features=self.CATEGORICAL_COLS,
            datetime=self.DATETIME_COL,
        )
        Log().log.info(f"column_mapping {self.column_mapping}")

        # init monitoring
        self.features_and_target_monitor = ModelMonitoring(
            monitors=[DataDriftMonitor()]
        )
        self.model_performance_monitor = ModelMonitoring(
            monitors=[ClassificationPerformanceMonitor()]
        )

    def _process_curr_data(self, new_rows: pd.DataFrame):
        Log().log.info("_process_curr_data")
        label_data = read_label_data()
        if label_data is None:
            return False
        Log().log.info(label_data.info())

        merged_data = merge_request_with_label(new_rows, label_data)
        Log().log.info(merged_data.info())

        if not self.current_data is None:
            curr_data: pd.DataFrame = pd.concat(
                [self.current_data, merged_data], ignore_index=True
            )
        else:
            curr_data = merged_data
        Log().log.info(curr_data.info())

        curr_size = curr_data.shape[0]
        if curr_size > self.WINDOW_SIZE:
            curr_data.drop(
                index=list(range(0, curr_size - self.WINDOW_SIZE)), inplace=True
            )
            curr_data.reset_index(drop=True, inplace=True)
        Log().log.info(curr_data.info())

        self.current_data = curr_data
        Log().log.info(f"current_data {self.current_data}")

        if curr_size < self.WINDOW_SIZE:
            Log().log.info(
                f"Not enough data for measurement: {curr_size}/{self.WINDOW_SIZE} rows. Waiting for more data"
            )
            return False
        return True

    def _process_next_run(self):
        Log().log.info("_process_next_run")
        if not self.next_run is None and self.next_run > datetime.now():
            Log().log.info(f"Next run at {self.next_run}")
            return False

        self.next_run = datetime.now() + timedelta(seconds=self.RUN_PERIOD_SEC)
        return True

    def _execute_monitoring(self):
        Log().log.info("_execute_monitoring")
        self.features_and_target_monitor.execute(
            self.reference_data,
            self.current_data,
            self.column_mapping,
        )
        self.model_performance_monitor.execute(
            self.current_data,
            self.current_data,
            self.column_mapping,
        )

    def _process_metrics(self, evidently_metrics):
        for metric, value, labels in evidently_metrics:
            metric_key = f"evidently:{metric.name}"

            if not labels:
                labels = {}
            labels["dataset_name"] = MonitoringService.DATASET_NAME

            if isinstance(value, str):
                continue

            found = self.metrics.get(metric_key)
            if found is None:
                found = prometheus_client.Gauge(
                    metric_key, "", list(sorted(labels.keys()))
                )
                self.metrics[metric_key] = found

            try:
                found.labels(**labels).set(value)
                Log().log.info(
                    f"Metric {metric_key}: Set {labels} to {value} successful"
                )

            except ValueError as error:
                # ignore errors sending other metrics
                Log().log.error(
                    f"Value error for metric key {metric_key}, error: {error}"
                )

    def iterate(self, new_rows: pd.DataFrame):
        Log().log.info("iterate")
        if not self._process_curr_data(new_rows):
            return

        if not self._process_next_run():
            return

        self._execute_monitoring()

        Log().log.info("_process_metrics features_and_target_monitor.metrics")
        self._process_metrics(self.features_and_target_monitor.metrics())

        Log().log.info("_process_metrics model_performance_monitor.metrics")
        self._process_metrics(self.model_performance_monitor.metrics())


SERVICE = MonitoringService()


@app.route("/iterate", methods=["POST"])
def iterate():
    item = flask.request.json
    Log().log.info(f"receive item {item}")

    df = pd.DataFrame.from_dict(item)
    Log().log.info(f"df {df}")

    SERVICE.iterate(new_rows=df)
    return "ok"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8309,
    )
    args = parser.parse_args()
    Log().log.info(f"args {args}")
    app.run(host="0.0.0.0", port=args.port, debug=True)
