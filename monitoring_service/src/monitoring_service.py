from datetime import datetime, timedelta
from typing import Optional

import flask
import pandas as pd
import prometheus_client
from evidently.model_monitoring import (
    CatTargetDriftMonitor,
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


class MonitoringService:
    WINDOW_SIZE = 5
    RUN_PERIOD_SEC = 15
    DATETIME_COL = "datetime"
    NUMERICAL_COLS = ["conv_rate", "acc_rate", "avg_daily_trips"]
    CATEGORICAL_COLS = []
    TARGET_COL = "trip_completed"
    PREDICTION_COL = "prediction"

    def __init__(self) -> None:
        self.next_run = None
        self.reference_data = None
        self.current_data = None

        # init column mapping
        self.column_mapping = ColumnMapping(
            target=self.TARGET_COL,
            prediction=self.PREDICTION_COL,
            numerical_features=self.NUMERICAL_COLS,
            categorical_features=self.CATEGORICAL_COLS,
            datetime=self.DATETIME_COL,
        )

        # init monitoring
        self.monitoring = ModelMonitoring(
            monitors=[
                DataDriftMonitor(),
                ClassificationPerformanceMonitor(),
            ],
            options=[],
        )

    def _read_label_data(self):
        label_file = AppPath.REQUEST_DATA
        if not label_file.exists():
            return None

        label_data = pd.read_csv(label_file)
        return label_data

    def _merge_request_with_label(
        self, new_rows: pd.DataFrame, label_data: pd.DataFrame
    ) -> pd.DataFrame:
        merged_data = pd.merge(
            left=new_rows, right=label_data, how="inner", on="request_id"
        )
        merged_data["prediction"] = 1
        return merged_data

    def _process_curr_data(self, new_rows: pd.DataFrame):
        label_data = self._read_label_data()
        if label_data is None:
            return False
        Log().log.info(label_data.info())

        merged_data = self._merge_request_with_label(new_rows, label_data)
        Log().log.info(merged_data.info())

        if not self.current_data is None:
            curr_data: pd.DataFrame = pd.concat([self.current_data, merged_data])
        else:
            curr_data = merged_data
        curr_size = curr_data.shape[0]

        if curr_size > self.WINDOW_SIZE:
            curr_data.drop(
                index=list(range(0, curr_size - self.WINDOW_SIZE)), inplace=True
            )
            curr_data.reset_index(drop=True, inplace=True)

        self.current_data = curr_data
        Log().log.info(f"current_data {self.current_data}")

        if curr_size < self.WINDOW_SIZE:
            Log().log.info(
                f"Not enough data for measurement: {curr_size}/{self.WINDOW_SIZE} rows. Waiting for more data"
            )
            return False
        return True

    def _process_next_run(self):
        if not self.next_run is None and self.next_run > datetime.now():
            Log().log.info(f"Next run at {self.next_run}")
            return False

        self.next_run = datetime.now() + timedelta(seconds=self.RUN_PERIOD_SEC)
        return True

    def _process_metrics(self):
        for metric, value, labels in self.monitoring.metrics():
            report = f"{metric.name} | {value} | {labels}"
            Log().log.info(report)

    def iterate(self, new_rows: pd.DataFrame):
        if not self._process_curr_data(new_rows):
            return

        if not self._process_next_run():
            return

        self.monitoring.execute(
            self.reference_data,
            self.current_data,
            self.column_mapping,
        )

        self._process_metrics()


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
    app.run(host="0.0.0.0", port=8309, debug=True)
