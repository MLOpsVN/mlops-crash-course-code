SHELL=/bin/bash

ENV_FILE="./deployment/.env"

feast_apply:
	source ${ENV_FILE} && bash scripts/feast_helper.sh apply

build_image:
	source ${ENV_FILE} && bash deployment/deploy.sh build

build_push_image:
	source ${ENV_FILE} && bash deployment/deploy.sh build_push

deploy_dags:
	source ${ENV_FILE} && bash deployment/deploy.sh dags

deploy_feature_repo:
	source ${ENV_FILE} && bash deployment/deploy.sh feature_repo
