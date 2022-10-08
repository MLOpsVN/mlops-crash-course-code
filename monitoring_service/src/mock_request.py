import argparse
import ast
import json
import subprocess
import time

import numpy as np
import pandas as pd
import requests

from utils import *

Log(AppConst.MOCK_REQUEST)
AppPath()

ONLINE_SERVING_API = "http://localhost:8172/inference"
MIN_DELAY_SEC = 1
MAX_DELAY_SEC = 2


def construct_request(row: pd.Series) -> dict:
    request_id = row["request_id"]
    driver_ids = ast.literal_eval(row["driver_ids"])
    return {
        "request_id": request_id,
        "driver_ids": driver_ids,
    }


def send_request(request: dict) -> None:
    Log().log.info(f"start send_request")

    try:
        data = json.dumps(request)
        Log().log.info(f"sending {data}")
        response = requests.post(
            ONLINE_SERVING_API,
            data=data,
            headers={"content-type": "application/json"},
        )

        if response.status_code == 200:
            Log().log.info(f"Success.")
        else:
            Log().log.info(
                f"Status code: {response.status_code}. Reason: {response.reason}, error text: {response.text}"
            )

    except Exception as error:
        Log().log.info(f"Error: {error}")


def main(data_type: str, n_request: int = 1):
    Log().log.info(f"load data")
    data_path = AppPath.NORMAL_DATA
    if data_type == DataType.DRIFT:
        data_path = AppPath.DRIFT_DATA
    data_source = pd.read_parquet(data_path, engine="fastparquet")
    request_data = pd.read_csv(AppPath.REQUEST_DATA)

    Log().log.info(f"write data_source to {AppPath.FEAST_DATA_SOURCE}")
    if AppPath.FEAST_DATA_SOURCE.exists():
        os.remove(AppPath.FEAST_DATA_SOURCE)
    data_source.to_parquet(AppPath.FEAST_DATA_SOURCE, engine="fastparquet")

    Log().log.info(f"run feast_teardown")
    result = subprocess.run(["make", "feast_teardown"])
    if result.returncode != 0:
        raise Exception("Failed to run feast_teardown")

    Log().log.info(f"run feast_apply")
    result = subprocess.run(["make", "feast_apply"])
    if result.returncode != 0:
        raise Exception("Failed to run feast_apply")

    Log().log.info(f"run feast_materialize")
    result = subprocess.run(["make", "feast_materialize"])
    if result.returncode != 0:
        raise Exception("Failed to run feast_materialize")

    Log().log.info(f"Send request to online serving API")

    Log().log.info(f"Start sending {n_request} requests")
    total_request = request_data.shape[0]
    for idx in range(n_request):
        Log().log.info(f"Sending request {idx+1}/{n_request}")
        row = request_data.iloc[idx % total_request]
        request = construct_request(row)
        send_request(request)
        delay_sec = np.random.uniform(low=MIN_DELAY_SEC, high=MAX_DELAY_SEC)
        Log().log.info(f"Wait {delay_sec} seconds")
        time.sleep(delay_sec)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--data_type",
        type=str,
        default=DataType.NORMAL,
        help=f"values=[{DataType.NORMAL}, {DataType.DRIFT}]",
    )
    parser.add_argument(
        "-n",
        "--n_request",
        type=int,
        default=10,
    )
    args = parser.parse_args()
    Log().log.info(f"args {args}")
    main(args.data_type, args.n_request)
