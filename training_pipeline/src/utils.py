import logging
import os
import sys
from pathlib import Path


class AppConst:
    LOG_LEVEL = logging.DEBUG
    DATA_EXTRACTION = "data_extraction"
    DATA_VALIDATION = "data_validation"
    DATA_PREPARATION = "data_preparation"
    MODEL_TRAINING = "model_training"
    MODEL_EVALUATION = "model_evaluation"
    MODEL_VALIDATION = "model_validation"


class AppPath:
    ROOT = Path("/training_pipeline")
    DATA = ROOT / "data"
    ARTIFACTS = ROOT / "artifacts"
    FEATURE_REPO = ROOT / "feature_repo"


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
    paths = os.listdir(path)
    for path in paths:
        Log().log.info(path)
