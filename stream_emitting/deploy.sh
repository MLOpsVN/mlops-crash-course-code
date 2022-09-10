#!/bin/bash

cmd=$1
tag=$2

# dockerhub username
DOCKER_USER="mlopsvn"
PROJECT="mlops_crash_course"
IMAGE_NAME="stream_emitting"

usage() {
    echo "deploy.sh"
}

build() {
    docker build --tag $DOCKER_USER/$PROJECT/$IMAGE_NAME:$tag .
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