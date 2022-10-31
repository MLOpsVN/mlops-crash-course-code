#!/bin/bash

cmd=$1

# constants
DOCKER_USER="$DOCKER_USER"
PROJECT="mlops_crash_course"
IMAGE_NAME="model_serving"
IMAGE_TAG=$(git describe --always)

if [[ -z "$DOCKER_USER" ]]; then
    echo "Missing \$DOCKER_USER env var"
    exit 1
fi

usage() {
    echo "deploy.sh <command> <arguments>"
    echo "Available commands:"
    echo " build                build image"
    echo " push                 push image"
    echo " build_push           build and push image"
    echo " compose_up           up docker compose"
    echo " compose_down         down docker compose"
    echo " dags                 deploy airflow dags"
    echo "Available arguments:"
    echo " [dags dir]           airflow dags directory, for command dags only"
}

if [[ -z "$cmd" ]]; then
    echo "Missing command"
    usage
    exit 1
fi

build() {
    docker build --tag $DOCKER_USER/$PROJECT/$IMAGE_NAME:$IMAGE_TAG -f deployment/Dockerfile .
    docker tag $DOCKER_USER/$PROJECT/$IMAGE_NAME:$IMAGE_TAG $DOCKER_USER/$PROJECT/$IMAGE_NAME:latest
}

push() {
    docker push $DOCKER_USER/$PROJECT/$IMAGE_NAME:$IMAGE_TAG
    docker push $DOCKER_USER/$PROJECT/$IMAGE_NAME:latest
}

compose_up() {
    # escape slash /
    FEAST_ONLINE_STORE_HOST=$(echo ${FEAST_ONLINE_STORE_HOST} | sed -e "s#/#\\\/#g")
    # replace value
    sed -i '' -e s/localhost/${FEAST_ONLINE_STORE_HOST}/ ./feature_repo/feature_store.yaml

    docker-compose --env-file ./deployment/.env -f ./deployment/docker-compose.yml up -d
}

compose_down() {
    # escape slash /
    FEAST_ONLINE_STORE_HOST=$(echo ${FEAST_ONLINE_STORE_HOST} | sed -e "s#/#\\\/#g")
    # replace value
    sed -i '' -e s/${FEAST_ONLINE_STORE_HOST}/localhost/ ./feature_repo/feature_store.yaml

    docker-compose --env-file ./deployment/.env -f ./deployment/docker-compose.yml down
}

deploy_dags() {
    if [[ -z "$DAGS_DIR" ]]; then
        echo "Missing DAGS_DIR env var"
        usage
        exit 1
    fi

    mkdir -p "$DAGS_DIR"
    cp dags/* "$DAGS_DIR"
}

shift

case $cmd in
build)
    build "$@"
    ;;
push)
    push "$@"
    ;;
build_push)
    build "$@"
    push "$@"
    ;;
compose_up)
    compose_up "$@"
    ;;
compose_down)
    compose_down "$@"
    ;;
dags)
    deploy_dags "$@"
    ;;
*)
    echo -n "Unknown command: $cmd"
    usage
    exit 1
    ;;
esac
