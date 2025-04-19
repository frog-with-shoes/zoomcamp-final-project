# zoomcamp-final-project


# Airflow Project Setup

This project requires a Google Cloud connection to be set up in Airflow.

## Google Cloud Connection Setup

1.  Create a Google Cloud service account with the necessary permissions (e.g., Storage Object Admin, bigquery).
2.  Download the service account key JSON file.


## Airflow Setup with docker compose

1. Install if you haven't docker, to be able to use docker compose.
2. git clone the repo.
3. Setup your environment variables, create your .env file.
4. docker compose build
5. docker compose up -d
6. Navigate to http://localhost:8080/ to access the Airflow UI.
7. navigate to Admin > Connections.
8. Create a new connection with the following details:
    * **Conn Id:** `google_cloud_default`
    * **Conn Type:** `Google Cloud`
    * **Project Id:** Your Google Cloud Project ID.
    * **Keyfile JSON:** Paste the contents of your service account key JSON file.
9. Save the connection.
10. From the airflow ui start the dag which will run the ELT pipeline.

## Terraform Setup

1. Create 

### Project structure
~~~
final-project
├── dags/
    └── src         # Example DAG file(s) you create
        └── ingest_spark_gcp.py # Ingestion script
│   └── upload_dag.py          # DAG definition.
├── .env.example               # Environment variables for Airflow and Docker Compose sample
├── final_project_dbt_transformation # dbt project
├── docker-compose.yml         # Docker Compose configuration file for Airflow services.
├── terraform                  # Contains file to provision the infrastructure, fill out variables_example.tf
├── README.md                  # This README file contains instruction to setup the project and the Problem description.
└── requirements.txt           # Additional Python dependencies
└── dashboard_tree_species_analysis _since_2000.pdf # Dashboard saved as pdf. Link to the dashboard: https://lookerstudio.google.com/s/taDt7fYj-MM
~~~


### Problem Description.

The purpose of building this ELT is build an ELT that:
1. Ingests the "arbres publics" dataset from the following website: https://donnees.montreal.ca/dataset/arbres. The first task seeks to place the ingestion script in a bucket. From there, we are able to call it using a local spark instance with gcs connector.
2. Loading the the buckets in parquet format to bigquery by partition by date planted and by species.
3. Transformation done through dbt core, it first creates a staging table to rename and filter our null values. Then it the fact table is called containing aggregations which can then be used to create the dashboard. 

The insight sought after from creating and running the pipeline is viewing the number of trees over time (20 years set by default). So a timeseries graph was used to evaluate that, moreover another tile showing the distribution of the species of trees was studied as well.