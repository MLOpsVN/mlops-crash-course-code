#!/bin/bash

cmd=$1

# constants
DOCKER_USER="$DOCKER_USER"
PROJECT="mlops_crash_course"
IMAGE_NAME="data_pipeline"
IMAGE_TAG=$(git describe --always)

if [[ -z "$DOCKER_USER" ]]; then
    echo "Missing \$DOCKER_USER env var"
    exit 1
fi

usage() {
    echo "deploy.sh <command>"
    echo "Available commands:"
    echo " build                build image"
    echo " push                 push image"
    echo " build_push           build and push image"
    echo " dags                 deploy airflow dags"
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

deploy_dags() {
    dags_dir=$1
    mkdir -p "$dags_dir"
    cp dags/* "$dags_dir"
}

deploy_feature_repo() {
    rsync -avr data_sources ../training_pipeline
    rsync -avr feature_repo ../training_pipeline --exclude registry

    rsync -avr data_sources ../model_serving
    rsync -avr feature_repo ../model_serving --exclude registry
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
dags)
    deploy_dags "$@"
    ;;
feature_repo)
    deploy_feature_repo "$@"
    ;;
*)
    echo -n "Unknown command: $cmd"
    usage
    exit 1
    ;;
esac
