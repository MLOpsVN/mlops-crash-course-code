SHELL=/bin/bash

ENV_FILE="./deployment/.env"

feast_apply:
	source ${ENV_FILE} && bash scripts/feast_helper.sh apply

feast_materialize:
	source ${ENV_FILE} && bash scripts/feast_helper.sh materialize

build_image:
	source ${ENV_FILE} && bash deployment/deploy.sh build

build_push_image:
	source ${ENV_FILE} && bash deployment/deploy.sh build_push

mock_request:
	python src/mock_request.py
