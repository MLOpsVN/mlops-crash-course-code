import pendulum

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

DATA_PIPELINE_TAG = "latest"

with DAG(
    dag_id='db_to_offline_store',
    schedule_interval="@once",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
) as dag:
    ingest_task = DockerOperator(
        task_id='ingest_task',
        image=f'mlopsvn/mlops_crash_coursedata_pipeline:{DATA_PIPELINE_TAG}',
        api_version='auto',
        auto_remove=True,
        command="/bin/bash -c 'cd scripts/db_to_offline_store && python ingest.py'",
    )

    clean_task = DockerOperator(
        task_id='clean_task',
        image=f'mlopsvn/mlops_crash_coursedata_pipeline:{DATA_PIPELINE_TAG}',
        api_version='auto',
        auto_remove=True,
        command="/bin/bash -c 'cd scripts/db_to_offline_store && python clean.py'",
    )

    explore_and_validate_task = DockerOperator(
        task_id='explore_and_validate_task',
        image=f'mlopsvn/mlops_crash_coursedata_pipeline:{DATA_PIPELINE_TAG}',
        api_version='auto',
        auto_remove=True,
        command="/bin/bash -c 'cd scripts/db_to_offline_store && python explore_and_validate.py'",
    )

    ingest_task >> clean_task >> explore_and_validate_task