FROM apache/airflow:3.3.0

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

COPY . /opt/airflow/project

ENV AIRFLOW_HOME=/opt/airflow

WORKDIR /opt/airflow/project
