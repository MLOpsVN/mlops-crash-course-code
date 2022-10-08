import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

import pendulum

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

from utils import *

with DAG(
    dag_id="db_to_offline_store",
    default_args=DefaultConfig.DEFAULT_DAG_ARGS,
    schedule_interval="@once",
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    tags=["data_pipeline"],
) as dag:
    ingest_task = DockerOperator(
        task_id="ingest_task",
        **DefaultConfig.DEFAULT_DOCKER_OPERATOR_ARGS,
        command="/bin/bash -c 'cd src/db_to_offline_store && python ingest.py'",
    )

    clean_task = DockerOperator(
        task_id="clean_task",
        **DefaultConfig.DEFAULT_DOCKER_OPERATOR_ARGS,
        command="/bin/bash -c 'cd src/db_to_offline_store && python clean.py'",
    )

    explore_and_validate_task = DockerOperator(
        task_id="explore_and_validate_task",
        **DefaultConfig.DEFAULT_DOCKER_OPERATOR_ARGS,
        command="/bin/bash -c 'cd src/db_to_offline_store && python explore_and_validate.py'",
    )

    ingest_task >> clean_task >> explore_and_validate_task