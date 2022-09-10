#!/bin/bash

cmd=$1
tag=$2

# dockerhub username
DOCKER_USER="mlopsvn"
PROJECT="mlops_crash_course"
IMAGE_NAME="data_pipeline"

usage() {
    echo "deploy.sh <command> <tag>"
    echo "Available commands:"
    echo " build                build image"
    echo " push                 push image"
    echo " all                  build and push image"
}

if [[ -z "$cmd" ]]; then
    echo "Missing command"
    usage
    exit 1
fi

if [[ -z "$tag" ]]; then
    echo "Missing tag"
    usage
    exit 1
fi

build() {
    cp -r feature_repo data scripts deployment
    docker build --tag $DOCKER_USER/$PROJECT/$IMAGE_NAME:$tag deployment
}

push() {
    docker push $DOCKER_USER/$PROJECT/$IMAGE_NAME:$tag
}

case $cmd in 
    build)
        build
        ;;
    push)
        push
        ;;
    all)
        build
        push
        ;;
    *)
        echo -n "Unknown command: $cmd"
        ;;
esac