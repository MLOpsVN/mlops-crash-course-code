import pendulum
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator


IMAGE_PATH = f"mlopsvn/training_pipeline:latest"

default_args = {
    "owner": "mlopsvn",
    "retries": 1,
    "retry_delay": pendulum.duration(seconds=20),
}

default_docker_operator_args = {
    "image": f"{IMAGE_PATH}",
    "api_version": "auto",
    "auto_remove": True,
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
        command="echo data_extraction_task",
        **default_docker_operator_args,
    )

    data_validation_task = DockerOperator(
        task_id="data_validation_task",
        command="echo data_validation_task",
        **default_docker_operator_args,
    )

    data_preparation_task = DockerOperator(
        task_id="data_preparation_task",
        command="echo data_preparation_task",
        **default_docker_operator_args,
    )

    model_training_task = DockerOperator(
        task_id="model_training_task",
        command="echo model_training_task",
        **default_docker_operator_args,
    )

    model_evaluation_task = DockerOperator(
        task_id="model_evaluation_task",
        command="echo model_evaluation_task",
        **default_docker_operator_args,
    )

    model_validation_task = DockerOperator(
        task_id="model_validation_task",
        command="echo model_validation_task",
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
