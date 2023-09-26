FROM python:3.8.8

COPY ./requirements.txt .

RUN apt-get update && apt-get install -y openjdk-11-jdk
RUN apt update && apt install -y tk-dev liblzma-dev libbz2-dev python3-dev python3-pip

RUN pip install -r requirements.txt

COPY . /training_pipeline

WORKDIR /training_pipeline

ENV AIRFLOW_HOME=$(pwd)
EXPOSE 8080
EXPOSE 3306