#!/bin/bash

IMAGE_NAME="mlopsvn/training_pipeline"
IMAGE_TAG=$(git describe --always)

echo "build"
docker build --tag $IMAGE_NAME:$IMAGE_TAG -f ./deployment/Dockerfile . --no-cache
docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest

echo "push"
docker push $IMAGE_NAME:$IMAGE_TAG
docker push $IMAGE_NAME:latest
