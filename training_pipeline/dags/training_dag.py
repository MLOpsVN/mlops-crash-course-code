import pendulum
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount


IMAGE_PATH = "mlopsvn/training_pipeline:latest"

default_args = {
    "owner": "mlopsvn",
    "retries": 0,
    "retry_delay": pendulum.duration(seconds=20),
}

default_docker_operator_args = {
    "image": IMAGE_PATH,
    "api_version": "auto",
    "auto_remove": True,
    # "mounts": [
    #     Mount(
    #         source="./run_env",
    #         target="/training_pipeline/data:rw",
    #         type="bind",
    #     )
    # ],
}

with DAG(
    dag_id="training_pipeline",
    default_args=default_args,
    schedule_interval="@once",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
) as dag:
    data_extraction_task = DockerOperator(
        task_id="data_extraction_task",
        command="python src/data_extraction.py",
        **default_docker_operator_args,
    )

    data_validation_task = DockerOperator(
        task_id="data_validation_task",
        command="python src/data_validation.py",
        **default_docker_operator_args,
    )

    data_preparation_task = DockerOperator(
        task_id="data_preparation_task",
        command="python src/data_preparation.py",
        **default_docker_operator_args,
    )

    model_training_task = DockerOperator(
        task_id="model_training_task",
        command="python src/model_training.py",
        **default_docker_operator_args,
    )

    model_evaluation_task = DockerOperator(
        task_id="model_evaluation_task",
        command="python src/model_evaluation.py",
        **default_docker_operator_args,
    )

    model_validation_task = DockerOperator(
        task_id="model_validation_task",
        command="python src/model_validation.py",
        **default_docker_operator_args,
    )

    (
        data_extraction_task
        >> data_validation_task
        >> data_preparation_task
        >> model_training_task
        >> model_evaluation_task
        >> model_validation_task
    )
