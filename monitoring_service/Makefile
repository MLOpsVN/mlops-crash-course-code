SHELL=/bin/bash

ENV_FILE="./deployment/.env"

feast_teardown:
	source ${ENV_FILE} && bash scripts/feast_helper.sh teardown

feast_apply:
	source ${ENV_FILE} && bash scripts/feast_helper.sh apply

feast_materialize:
	source ${ENV_FILE} && bash scripts/feast_helper.sh materialize

build_image:
	source ${ENV_FILE} && bash deployment/deploy.sh build

build_push_image:
	source ${ENV_FILE} && bash deployment/deploy.sh build_push

compose_up:
	source ${ENV_FILE} && bash deployment/deploy.sh compose_up

compose_down:
	source ${ENV_FILE} && bash deployment/deploy.sh compose_down
