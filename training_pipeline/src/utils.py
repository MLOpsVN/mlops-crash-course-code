import json
import logging
import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class AppConst:
    LOG_LEVEL = logging.DEBUG
    DATA_EXTRACTION = "data_extraction"
    DATA_VALIDATION = "data_validation"
    DATA_PREPARATION = "data_preparation"
    MODEL_TRAINING = "model_training"
    MODEL_EVALUATION = "model_evaluation"
    MODEL_VALIDATION = "model_validation"
    MLFLOW_MODEL_PATH_PREFIX = "model"


class AppPath:
    # set TRAINING_PIPELINE_DIR in dev environment for quickly testing the code
    ROOT = Path(os.environ.get("TRAINING_PIPELINE_DIR", "/training_pipeline"))
    DATA = ROOT / "data"
    DATA_SOURCES = ROOT / "data_sources"
    FEATURE_REPO = ROOT / "feature_repo"
    ARTIFACTS = ROOT / "artifacts"

    TRAINING_PQ = ARTIFACTS / "training.parquet"
    TRAIN_X_PQ = ARTIFACTS / "train_x.parquet"
    TRAIN_Y_PQ = ARTIFACTS / "train_y.parquet"
    TEST_X_PQ = ARTIFACTS / "test_x.parquet"
    TEST_Y_PQ = ARTIFACTS / "test_y.parquet"
    RUN_INFO = ARTIFACTS / "run_info.json"
    EVALUATION_RESULT = ARTIFACTS / "evaluation.json"
    REGISTERED_MODEL_VERSION = ARTIFACTS / "registered_model_version.json"

    def __init__(self) -> None:
        AppPath.ARTIFACTS.mkdir(parents=True, exist_ok=True)


class Config:
    def __init__(self) -> None:
        import numpy as np

        self.random_seed = int(os.environ.get("RANDOM_SEED"))
        self.feature_dict = {
            # "event_timestamp": pd.DatetimeTZDtype(tz="UTC"),
            # "driver_id": np.int64,
            "conv_rate": np.float64,
            "acc_rate": np.float64,
            "avg_daily_trips": np.int64,
            "trip_completed": np.int64,
        }
        self.target_col = os.environ.get("TARGET_COL")
        self.test_size = float(os.environ.get("TEST_SIZE"))
        self.experiment_name = os.environ.get("EXPERIMENT_NAME")
        self.mlflow_tracking_uri = os.environ.get("MLFLOW_TRACKING_URI")
        self.alpha = float(os.environ.get("ALPHA"))
        self.l1_ratio = float(os.environ.get("L1_RATIO"))
        self.rmse_threshold = float(os.environ.get("RMSE_THRESHOLD"))
        self.mae_threshold = float(os.environ.get("MAE_THRESHOLD"))
        self.registered_model_name = os.environ.get("REGISTERED_MODEL_NAME")


class RunInfo:
    def __init__(self, run_id) -> None:
        self.path = AppPath.RUN_INFO
        self.run_id = run_id

    def save(self):
        run_info = {
            "run_id": self.run_id,
        }
        dump_json(run_info, self.path)

    @staticmethod
    def load(path):
        data = load_json(path)
        run_info = RunInfo(data["run_id"])
        return run_info


class EvaluationResult:
    def __init__(self, rmse, mae) -> None:
        self.path = AppPath.EVALUATION_RESULT
        self.rmse = rmse
        self.mae = mae

    def __str__(self) -> str:
        return f"RMSE: {self.rmse}, MAE: {self.mae}"

    def save(self):
        eval_result = {
            "rmse": self.rmse,
            "mae": self.mae,
        }
        dump_json(eval_result, self.path)

    @staticmethod
    def load(path):
        data = load_json(path)
        eval_result = EvaluationResult(
            data["rmse"],
            data["mae"],
        )
        return eval_result


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
