import pendulum

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

DATA_PIPELINE_TAG = "0.0.1"

with DAG(
    dag_id='db_to_offline_store',
    schedule_interval="@once",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
) as dag:
    ingest_task = DockerOperator(
        task_id='ingest_task',
        image=f'dangvanquan25/data-pipeline:{DATA_PIPELINE_TAG}',
        api_version='auto',
        auto_remove=True,
        command="cd scripts/db_to_offline_store && python ingest.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
    )

    clean_task = DockerOperator(
        task_id='clean_task',
        image=f'dangvanquan25/data-pipeline:{DATA_PIPELINE_TAG}',
        api_version='auto',
        auto_remove=True,
        command="cd scripts/db_to_offline_store && python clean.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
    )

    explore_and_validate_task = DockerOperator(
        task_id='explore_and_validate_task',
        image=f'dangvanquan25/data-pipeline:{DATA_PIPELINE_TAG}',
        api_version='auto',
        auto_remove=True,
        command="cd scripts/db_to_offline_store && python explore_and_validate.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
    )

    ingest_task >> clean_task >> explore_and_validate_task