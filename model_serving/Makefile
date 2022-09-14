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

bentoml_serve:
	bash scripts/bentoml_helper.sh serve

compose_up:
	docker-compose -f ./deployment/docker-compose.yml up -d

compose_down:
	docker-compose -f ./deployment/docker-compose.yml down
