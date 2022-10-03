#!/bin/bash

cmd=$1

# constants
DOCKER_USER="$DOCKER_USER"
PROJECT="mlops_crash_course"
IMAGE_NAME="training_pipeline"
IMAGE_TAG=$(git describe --always)

if [[ -z "$DOCKER_USER" ]]; then
    echo "Missing \$DOCKER_USER env var"
    exit 1
fi

usage() {
    echo "deploy.sh <command> <arguments>"
    echo "Available commands:"
    echo " build                    build image"
    echo " push                     push image"
    echo " build_push               build and push image"
    echo " dags                     deploy airflow dags"
    echo " registered_model_file    deploy registered model file to model_serving"
    echo " training_set             upload train_x and train_y parquet files"
    echo "Available arguments:"
    echo " [dags dir]               airflow dags directory, for command dags only"
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
    if [[ -z "$DAGS_DIR" ]]; then
        echo "Missing DAGS_DIR env var"
        usage
        exit 1
    fi

    mkdir -p "$DAGS_DIR"
    cp dags/* "$DAGS_DIR"
}

deploy_registered_model_file() {
    registered_model_file="./artifacts/registered_model_version.json"
    if [[ ! -f "$registered_model_file" ]]; then
        echo "$registered_model_file doesn't exist"
        exit 1
    fi

    model_serving_artifacts_dir="../model_serving/artifacts/"
    cp "$registered_model_file" "$model_serving_artifacts_dir"
}

upload_training_set() {
    train_x="./artifacts/train_x.parquet"
    train_y="./artifacts/train_y.parquet"
    if [[ ! -f "$train_x" ]]; then
        echo "$train_x doesn't exist"
        exit 1
    fi
    if [[ ! -f "$train_y" ]]; then
        echo "$train_y doesn't exist"
        exit 1
    fi

    monitoring_service_data_dir="../monitoring_service/data/"
    cp "$train_x" "$monitoring_service_data_dir"
    cp "$train_y" "$monitoring_service_data_dir"
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
registered_model_file)
    deploy_registered_model_file "$@"
    ;;
training_set)
    upload_training_set "$@"
    ;;
*)
    echo -n "Unknown command: $cmd"
    usage
    exit 1
    ;;
esac
