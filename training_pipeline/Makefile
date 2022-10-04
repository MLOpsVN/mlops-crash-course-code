SHELL=/bin/bash

ENV_FILE="./deployment/.env"

feast_apply:
	source ${ENV_FILE} && cd feature_repo && feast apply

build_image:
	source ${ENV_FILE} && bash deployment/deploy.sh build

build_push_image:
	source ${ENV_FILE} && bash deployment/deploy.sh build_push

deploy_dags:
	source ${ENV_FILE} && bash deployment/deploy.sh dags

deploy_registered_model_file:
	source ${ENV_FILE} && bash deployment/deploy.sh registered_model_file
