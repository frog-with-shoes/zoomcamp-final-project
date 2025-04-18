FROM apache/airflow:2.10.5-python3.9

USER root 

RUN apt-get update && apt-get install -y curl gnupg build-essential python3-dev

RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

RUN echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

RUN apt-get update && apt-get install -y google-cloud-sdk

USER airflow

RUN pip uninstall -y pendulum
RUN pip cache purge
RUN pip install --no-cache-dir setuptools
RUN pip install --no-cache-dir pendulum==2.1.2

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt


COPY dags/ /app/dags/