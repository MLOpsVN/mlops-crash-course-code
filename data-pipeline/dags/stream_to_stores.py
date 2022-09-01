import datetime

import pendulum

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

with DAG(
    dag_id='stream_to_stores',
    schedule_interval="@once",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
) as dag:
    stream_to_online_task = DockerOperator(
        task_id='docker_command',
        image='centos:latest',
        api_version='auto',
        auto_remove=True,
        command="cd scripts/stream_to_stores && python ingest.py --store online",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
    )

    stream_to_offline_task = DockerOperator(
        task_id='docker_command',
        image='centos:latest',
        api_version='auto',
        auto_remove=True,
        command="cd scripts/stream_to_stores && python ingest.py --store offline",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
    )

    stop_stream_task = DockerOperator(
        task_id='docker_command',
        image='centos:latest',
        api_version='auto',
        auto_remove=True,
        command="cd scripts/stream_to_stores && python ingest.py --mode teardown",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
    )

    # to create dag and pass processor to stop_stream_task