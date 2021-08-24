FROM python:3.7.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "main.py"]