import json
import logging
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class AppConst:
    LOG_LEVEL = logging.DEBUG
    BENTOML_MODEL_SAVING = "bentoml_model_saving"
    BENTOML_SERVICE = "bentoml_service"
    DATA_EXTRACTION = "data_extraction"
    BATCH_PREDICTION = "batch_prediction"


class AppPath:
    # set MODEL_SERVING_DIR in dev environment for quickly testing the code
    ROOT = Path(os.environ.get("MODEL_SERVING_DIR", "/model_serving"))
    DATA = ROOT / "data"
    DATA_SOURCES = ROOT / "data_sources"
    FEATURE_REPO = ROOT / "feature_repo"
    ARTIFACTS = ROOT / "artifacts"

    BATCH_INPUT_PQ = ARTIFACTS / "batch_input.parquet"
    BATCH_OUTPUT_PQ = ARTIFACTS / "batch_output.parquet"

    def __init__(self) -> None:
        AppPath.ARTIFACTS.mkdir(parents=True, exist_ok=True)


class Config:
    def __init__(self) -> None:
        import numpy as np

        self.feature_dict = {
            "conv_rate": np.float64,
            "acc_rate": np.float64,
            "avg_daily_trips": np.int64,
            "trip_completed": np.int64,
        }
        self.mlflow_tracking_uri = os.environ.get("MLFLOW_TRACKING_URI")
        self.batch_input_file = os.environ.get("BATCH_INPUT_FILE")
        self.registered_model_file = os.environ.get("REGISTERED_MODEL_FILE")
        self.monitoring_service_api = os.environ.get("MONITORING_SERVICE_API")


class Log:
    log: logging.Logger = None

    def __init__(self, name="") -> None:
        if Log.log == None:
            Log.log = self._init_logger(name)

    def _init_logger(self, name):
        logger = logging.getLogger(name)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        logger.setLevel(AppConst.LOG_LEVEL)
        return logger


# the encoder helps to convert NumPy types in source data to JSON-compatible types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.void):
            return None

        if isinstance(obj, (np.generic, np.bool_)):
            return obj.item()

        if isinstance(obj, np.ndarray):
            return obj.tolist()

        return obj


def inspect_dir(path):
    Log().log.info(f"inspect_dir {path}")
    path = Path(path)
    if not path.exists():
        Log().log.info(f"Path {path} doesn't exist")
        return
    elif path.is_file():
        Log().log.info(f"Path {path} is file")
        return

    paths = os.listdir(path)
    paths = sorted(paths)
    for path in paths:
        Log().log.info(path)


def inspect_curr_dir():
    cwd = os.getcwd()
    Log().log.info(f"current dir: {cwd}")
    inspect_dir(cwd)


def load_df(path) -> pd.DataFrame:
    Log().log.info(f"start load_df {path}")
    df = pd.read_parquet(path, engine="fastparquet")
    return df


def to_parquet(df: pd.DataFrame, path):
    Log().log.info(f"start to_parquet {path}")
    df.to_parquet(path, engine="fastparquet")


def dump_json(dict_obj: dict, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dict_obj, f)


def load_json(path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
