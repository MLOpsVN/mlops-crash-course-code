from pathlib import Path

import pendulum
from airflow.models import Variable
from docker.types import Mount


class AppPath:
    ROOT = Path(Variable.get("ROOT_DIR"))
    ARTIFACTS = ROOT / "artifacts"
    FEATURE_STORE_ROOT = Path(Variable.get("FEATURE_STORE_ROOT_DIR"))


class DefaultConfig:
    DEFAULT_DAG_ARGS = {
        "owner": "mlopsvn",
        "retries": 0,
        "retry_delay": pendulum.duration(seconds=20),
    }

    DEFAULT_DOCKER_OPERATOR_ARGS = {
        "image": "mlopsvn/training_pipeline:latest",
        "api_version": "auto",
        "auto_remove": True,
        "mounts": [
            # artifacts
            Mount(
                source=AppPath.ARTIFACTS.as_posix(),
                target="/training_pipeline/artifacts",
                type="bind",
            ),
            # feature store
            Mount(
                source=AppPath.FEATURE_STORE_ROOT.as_posix(),
                target="/training_pipeline/feature_store",
                type="bind",
            ),
        ],
    }
