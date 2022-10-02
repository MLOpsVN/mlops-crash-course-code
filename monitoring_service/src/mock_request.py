import argparse
import ast
import json
import subprocess
import time

import pandas as pd
import requests

from utils import *

Log(AppConst.MOCK_REQUEST)
AppPath()

ONLINE_SERVING_API = "http://localhost:8172/inference"
DELAY_SEC = 1


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

    Log().log.info(f"write data_source to data_sources")
    if AppPath.FEAST_DATA_SOURCE.exists():
        os.remove(AppPath.FEAST_DATA_SOURCE)
    data_source.to_parquet(AppPath.FEAST_DATA_SOURCE, engine="fastparquet")

    # Log().log.info(f"run feast_apply")
    # result = subprocess.run(["make", "feast_apply"])
    # if result.returncode != 0:
    #     raise Exception("Failed to run feast_apply")

    # Log().log.info(f"run feast_materialize")
    # result = subprocess.run(["make", "feast_materialize"])
    # if result.returncode != 0:
    #     raise Exception("Failed to run feast_materialize")

    Log().log.info(f"Send request to online serving API")
    n_sent = min(n_request, request_data.shape[0])
    for idx in range(n_sent):
        row = request_data.iloc[idx]
        request = construct_request(row)
        send_request(request)
        Log().log.info(f"Wait {DELAY_SEC} seconds")
        time.sleep(DELAY_SEC)


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
        default=1,
    )
    args = parser.parse_args()
    main(args.data_type, args.n_request)
