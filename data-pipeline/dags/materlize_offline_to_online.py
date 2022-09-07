import datetime

import pendulum

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

DATA_PIPELINE_TAG = "0.0.1"

with DAG(
    dag_id='materlize_offline_to_online',
    schedule_interval="@once",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
) as dag:
    materialize_task = DockerOperator(
        task_id='materialize_task',
        image=f'dangvanquan25/data-pipeline:{DATA_PIPELINE_TAG}',
        api_version='auto',
        auto_remove=True,
        command="cd scripts/materlize_offline_to_online && bash materialize.sh",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
    )