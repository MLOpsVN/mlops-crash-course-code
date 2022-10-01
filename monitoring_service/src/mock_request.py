import argparse
import json
import time

import pandas as pd
import requests

from utils import *

Log(AppConst.MOCK_REQUEST)
AppPath()

DRIVER_IDS = [1001, 1002, 1003, 1004, 1005]


def construct_request(request_id: str, driver_ids: list) -> dict:
    return {
        "request_id": request_id,
        "driver_ids": driver_ids,
    }


def send_request(request: dict) -> None:
    print(f"start send_request")

    try:
        print(f"sending {request}")
        response = requests.post(
            f"http://localhost:8172/inference",
            data=json.dumps([request]),
            headers={"content-type": "application/json"},
        )

        if response.status_code == 200:
            print(f"Success.")
        else:
            print(
                f"Status code: {response.status_code}. Reason: {response.reason}, error text: {response.text}"
            )

    except Exception as error:
        print(f"Error: {error}")


def main(data_type: str):
    # load request data
    data_path = AppPath.NORMAL_DATA
    if data_type == DataType.DRIFT:
        data_path = AppPath.DRIFT_DATA
    dataset = pd.read_parquet(data_path, engine="fastparquet")

    # update data source for selected data type

    # update label file for selected data type

    # run feast apply & materialize

    for idx in range(dataset.shape[0]):
        row = dataset.iloc[idx]
        request = construct_request(row["request_id"], DRIVER_IDS)
        send_request(request)
        print(f"Wait {AppConst.DELAY_SEC} seconds till the next try")
        time.sleep(AppConst.DELAY_SEC)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--data_type",
        type=str,
        default=DataType.NORMAL,
        help=f"values=[{DataType.NORMAL}, {DataType.DRIFT}]",
    )
    args = parser.parse_args()
    main(args["data_type"])
