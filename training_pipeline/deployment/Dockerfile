FROM python:3.8-slim

RUN apt-get update && rm -rf /var/lib/apt/lists/*

WORKDIR /training_pipeline

COPY ./requirements.txt /training_pipeline/requirements.txt

RUN pip3 install -r /training_pipeline/requirements.txt

COPY . /training_pipeline
