import pendulum
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

from utils import *


with DAG(
    dag_id="training_pipeline",
    default_args=DefaultConfig.DEFAULT_DAG_ARGS,
    schedule_interval="@once",
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
) as dag:
    data_extraction_task = DockerOperator(
        task_id="data_extraction_task",
        command="python src/data_extraction.py",
        **DefaultConfig.DEFAULT_DOCKER_OPERATOR_ARGS,
    )

    data_validation_task = DockerOperator(
        task_id="data_validation_task",
        command="python src/data_validation.py",
        **DefaultConfig.DEFAULT_DOCKER_OPERATOR_ARGS,
    )

    data_preparation_task = DockerOperator(
        task_id="data_preparation_task",
        command="python src/data_preparation.py",
        **DefaultConfig.DEFAULT_DOCKER_OPERATOR_ARGS,
    )

    model_training_task = DockerOperator(
        task_id="model_training_task",
        command="python src/model_training.py",
        **DefaultConfig.DEFAULT_DOCKER_OPERATOR_ARGS,
    )

    model_evaluation_task = DockerOperator(
        task_id="model_evaluation_task",
        command="python src/model_evaluation.py",
        **DefaultConfig.DEFAULT_DOCKER_OPERATOR_ARGS,
    )

    model_validation_task = DockerOperator(
        task_id="model_validation_task",
        command="python src/model_validation.py",
        **DefaultConfig.DEFAULT_DOCKER_OPERATOR_ARGS,
    )

    (
        data_extraction_task
        >> data_validation_task
        >> data_preparation_task
        >> model_training_task
        >> model_evaluation_task
        >> model_validation_task
    )
