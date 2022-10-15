import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

import pendulum

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

from utils import *

with DAG(
    dag_id="materlize_offline_to_online",
    default_args=DefaultConfig.DEFAULT_DAG_ARGS,
    schedule_interval="@once",
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    tags=["data_pipeline"],
) as dag:
    materialize_task = DockerOperator(
        task_id="materialize_task",
        **DefaultConfig.DEFAULT_DOCKER_OPERATOR_ARGS,
<<<<<<< HEAD
<<<<<<< HEAD
        command="/bin/bash -c 'chmod +x ./scripts/feast_helper.sh' && ./scripts/feast_helper.sh",
    )
=======
        command="/bin/bash ./scripts/feast_helper.sh materialize",
    )
>>>>>>> main
=======
        command="/bin/bash ./scripts/feast_helper.sh materialize",
    )
>>>>>>> main
