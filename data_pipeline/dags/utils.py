import pendulum


class DefaultConfig:
    DEFAULT_DAG_ARGS = {
        "owner": "mlopsvn",
        "retries": 0,
        "retry_delay": pendulum.duration(seconds=20),
    }

    DEFAULT_DOCKER_OPERATOR_ARGS = {
        "image": "mlopsvn/mlops_crash_course/data_pipeline:latest",
        "api_version": "auto",
        "auto_remove": True,
    }