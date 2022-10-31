from pathlib import Path

import pendulum
from airflow.models import Variable
from docker.types import Mount


class AppConst:
    DOCKER_USER = Variable.get("DOCKER_USER", "mlopsvn")


class AppPath:
    MLOPS_CRASH_COURSE_CODE_DIR = Path(Variable.get("MLOPS_CRASH_COURSE_CODE_DIR"))
    TRAINING_PIPELINE_DIR = MLOPS_CRASH_COURSE_CODE_DIR / "training_pipeline"
    FEATURE_REPO = TRAINING_PIPELINE_DIR / "feature_repo"
    ARTIFACTS = TRAINING_PIPELINE_DIR / "artifacts"


class DefaultConfig:
    DEFAULT_DAG_ARGS = {
        "owner": "mlopsvn",
        "retries": 0,
        "retry_delay": pendulum.duration(seconds=20),
    }

    DEFAULT_DOCKER_OPERATOR_ARGS = {
        "image": f"{AppConst.DOCKER_USER}/mlops_crash_course/training_pipeline:latest",
        "api_version": "auto",
        "auto_remove": True,
        "network_mode": "bridge",
        "docker_url": "tcp://docker-proxy:2375",
        "mounts": [
            # feature repo
            Mount(
                source=AppPath.FEATURE_REPO.absolute().as_posix(),
                target="/training_pipeline/feature_repo",
                type="bind",
            ),
            # artifacts
            Mount(
                source=AppPath.ARTIFACTS.absolute().as_posix(),
                target="/training_pipeline/artifacts",
                type="bind",
            ),
        ],
    }
