SHELL=/bin/bash

ENV_FILE=.env
PUSH_IMAGE=""
DAGS_DIR="../../mlops-crash-course-platform/airflow/run_env/dags/data_pipeline"

feast_apply:
	source ${ENV_FILE} && bash scripts/feast_helper.sh apply

build_image:
	source ${ENV_FILE} && bash deployment/deploy.sh build

build_push_image:
	source ${ENV_FILE} && bash deployment/deploy.sh build_push

deploy_dags:
	source ${ENV_FILE} && bash deployment/deploy.sh dags "${DAGS_DIR}"
