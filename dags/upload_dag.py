import os

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime
from src.ingest_spark_gcp import extract

from dotenv import load_dotenv

load_dotenv()
GCS_SOURCE_URI = os.getenv("GCP_PROJECT")


GCS_BUCKET = "dtc_data_lake_de_nytaxi_mee"
GCS_FILE_PATH = "code/trees_write_gcs_bucket_upload.py" # The new path
LOCAL_FILE_PATH = "/opt/airflow/dags/src/ingest_spark_gcp.py"

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

    load_to_bq = BigQueryInsertJobOperator(
        task_id='load_partitioned_data_to_bq',
        configuration={
            "load": {
                "sourceUris": [
                    "gs://dtc_data_lake_de_nytaxi_mee/pq/montreal_trees/*.parquet"
                ],
                "destinationTable": {
                    "projectId": GCS_SOURCE_URI,
                    "datasetId": "trips_data_all",
                    "tableId": "tree-report-partitioned-clustered"
                },
                "sourceFormat": "PARQUET",
                "writeDisposition": "WRITE_APPEND",
                "autodetect": True, 
                "timePartitioning": {
                "type": "MONTH",
                "field": "date_plantation",  
                "requirePartitionFilter": True  
                },
                "clustering": {
                    "fields": ["arrond_nom" , "Essence_latin"]  
                }
            }
        },
        location="US",
        gcp_conn_id="google_cloud_default",
    )

    run_dbt_transformations = BashOperator(
        task_id='run_dbt_transformations',
        bash_command='cd /opt/airflow/dbt && dbt run --profiles-dir /opt/dbt/.dbt',
    )

    upload_with_operator  >> run_script_task >> load_to_bq >> run_dbt_transformations