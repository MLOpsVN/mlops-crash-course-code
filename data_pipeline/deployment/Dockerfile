FROM python:3.8-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         openjdk-11-jre-headless \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
  
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

WORKDIR /data-pipeline

COPY . /data-pipeline

RUN pip3 install -r /data-pipeline/requirements.txt

