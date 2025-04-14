FROM apache/airflow:2.10.5
RUN pip install pyspark
COPY lib/gcs-connector-hadoop3-2.2.5.jar /opt/airflow/jars/gcs-connector-hadoop3-2.2.5.jar

# install java and set up path...