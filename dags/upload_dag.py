import os

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from datetime import datetime
from src.ingest_spark_gcp import extract
GCS_BUCKET = "dtc_data_lake_de_nytaxi_mee"
GCS_FILE_PATH = "code/trees_write_gcs_bucket_upload.py" # The new path
LOCAL_FILE_PATH = "/opt/airflow/dags/src/trees_write_gcs_bucket_upload.py"

with DAG(
    dag_id='upload_to_gcs',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['gcs']
) as dag:

    upload_with_operator = LocalFilesystemToGCSOperator(
        task_id='upload_with_operator',
        src=LOCAL_FILE_PATH,
        dst=GCS_FILE_PATH,
        bucket=GCS_BUCKET,
        dag=dag,
    )

    run_script_task = PythonOperator(
        task_id='run_my_external_script',
        python_callable=extract,
    )

    upload_with_operator  >> run_script_task