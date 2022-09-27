from datetime import datetime, timedelta
from typing import Dict, List, Optional

import hashlib
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


class MonitoringService:
    def __init__(self) -> None:
        self.window_size = 5
        self.next_run = None
        self.run_period_sec = 15

        self.reference_data = None
        self.current_data = None

        # init column mapping
        numerical_features = ["conv_rate", "acc_rate", "avg_daily_trips"]
        categorical_features = []
        target = "trip_completed"
        self.column_mapping = ColumnMapping(
            target=target,
            numerical_features=numerical_features,
            categorical_features=categorical_features,
            datetime="datetime",
        )

        # init monitoring
        self.monitoring = ModelMonitoring(
            monitors=[
                DataDriftMonitor(),
                ClassificationPerformanceMonitor(),
                CatTargetDriftMonitor(),
            ],
            options=[],
        )

    def _process_curr_data(self, new_rows: pd.DataFrame):
        curr_data: pd.DataFrame = pd.concat([self.current_data, new_rows])
        curr_size = curr_data.shape[0]

        if curr_size > self.window_size:
            # cut current_size by window size value
            curr_data.drop(
                index=list(range(0, curr_size - self.window_size)), inplace=True
            )
            curr_data.reset_index(drop=True, inplace=True)
        self.current_data = curr_data

        if curr_size < self.window_size:
            Log().log.info(
                f"Not enough data for measurement: {curr_size}/{self.window_size} rows. Waiting for more data"
            )
            return False
        return True

    def _process_next_run(self):
        if not self.next_run is None and self.next_run > datetime.now():
            Log().log.info(f"Next run at {self.next_run}")
            return False

        self.next_run = datetime.now() + timedelta(seconds=self.run_period_sec)
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


# - Ở monitoring service:
#     - Ingest request data vào feature store
#         - Để compare với training data later
#     - Lưu request id + response data vào disk
#         - Để compare với label later
# - Data drift detection
#     - Detect feature drift
#     - Send metrics to Prom để visualize metrics
#     - Setup alert
# - Target drift detection
#     - Giả sử có label rồi, lấy từ file từ disk
#         - Dựa vào nbs trên để lấy label
#     - Report model performance giữa response data và label
#     - Detect target drift
#     - Send metrics to Prom để visualize metrics
#     - Setup alert
