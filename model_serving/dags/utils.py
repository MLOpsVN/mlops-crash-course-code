from pathlib import Path

import pendulum
from airflow.models import Variable
from docker.types import Mount


class AppConst:
    DOCKER_USER = Variable.get("DOCKER_USER", "mlopsvn")


class AppPath:
    MLOPS_CRASH_COURSE_CODE_DIR = Path(Variable.get("MLOPS_CRASH_COURSE_CODE_DIR"))
    MODEL_SERVING_DIR = MLOPS_CRASH_COURSE_CODE_DIR / "model_serving"
    FEATURE_REPO = MODEL_SERVING_DIR / "feature_repo"
    ARTIFACTS = MODEL_SERVING_DIR / "artifacts"
    DATA = MODEL_SERVING_DIR / "data"


class DefaultConfig:
    DEFAULT_DAG_ARGS = {
        "owner": "mlopsvn",
        "retries": 0,
        "retry_delay": pendulum.duration(seconds=20),
    }

    DEFAULT_DOCKER_OPERATOR_ARGS = {
        "image": f"{AppConst.DOCKER_USER}/mlops_crash_course/model_serving:latest",
        "api_version": "auto",
        "auto_remove": True,
        "network_mode": "bridge",
        "docker_url": "tcp://docker-proxy:2375",
        "mounts": [
            # feature repo
            Mount(
                source=AppPath.FEATURE_REPO.absolute().as_posix(),
                target="/model_serving/feature_repo",
                type="bind",
            ),
            # artifacts
            Mount(
                source=AppPath.ARTIFACTS.absolute().as_posix(),
                target="/model_serving/artifacts",
                type="bind",
            ),
            # data
            Mount(
                source=AppPath.DATA.absolute().as_posix(),
                target="/model_serving/data",
                type="bind",
            ),
        ],
    }
