FROM python:3.7-slim

RUN pip install "feast[redis]"

COPY feature_store.yaml feature_store.yaml

CMD ["feast", "serve", "-h", "0.0.0.0"]