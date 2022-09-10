FROM python:3.8-slim AS build

RUN apt-get update && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.8-slim

COPY --from=build /opt/venv /training_pipeline/venv
ENV PATH="/training_pipeline/venv/bin:$PATH"
COPY . /training_pipeline
WORKDIR /training_pipeline
