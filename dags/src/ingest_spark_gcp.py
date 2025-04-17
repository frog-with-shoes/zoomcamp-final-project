import json
import tempfile
import os
import logging

import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext

from airflow.hooks.base import BaseHook
from airflow.decorators import task
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# hello world 2
def extract():
    conn  = BaseHook.get_connection('google_cloud_default')
    keyfile_dict = json.loads(conn.extra_dejson.get("keyfile_dict"))
   
    logger.info("Writing GCP credentials to temporary file...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        json.dump(keyfile_dict, tmp)
        keyfile_path = tmp.name
        logger.info(f"Temporary keyfile written to: {keyfile_path}")

    try:
        conf = SparkConf() \
            .setMaster('local[*]') \
            .setAppName('test') \
            .set("spark.jars", "/opt/spark/jars/gcs-connector-hadoop3-2.2.5.jar") \
            .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
            .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", keyfile_path)




        sc = SparkContext.getOrCreate(conf=conf)

        hadoop_conf = sc._jsc.hadoopConfiguration()

        hadoop_conf.set("fs.AbstractFileSystem.gs.impl",  "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
        hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
        hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", keyfile_path)
        hadoop_conf.set("fs.gs.auth.service.account.enable", "true")




        spark = SparkSession.builder \
            .config(conf=sc.getConf()) \
            .getOrCreate()






        from pyspark.sql import types




        public_tree_schema = types.StructType([
        types.StructField('INV_TYPE', types.StringType(), True),
        types.StructField('EMP_NO', types.IntegerType(), True),
        types.StructField('ARROND', types.IntegerType(), True),
        types.StructField('ARROND_NOM', types.StringType(), True),
        types.StructField('Rue', types.StringType(), True),
        types.StructField('Rue_cote', types.StringType(), True),
        types.StructField('No_civique', types.StringType(), True),
        types.StructField('Emplacement', types.StringType(), True),
        types.StructField('Sigle', types.StringType(), True),
        types.StructField('Essence_latin', types.StringType(), True),
        types.StructField('Essence_fr', types.StringType(), True),
        types.StructField('Essence_ang', types.StringType(), True),
        types.StructField('DHP', types.StringType(), True),
        types.StructField('Date_Releve', types.TimestampType(), True),
        types.StructField('Date_Plantation', types.TimestampType(), True),
        types.StructField('LOCALISATION', types.StringType(), True),
        types.StructField('Localisation_code', types.StringType(), True),
        types.StructField('CODE_PARC', types.StringType(), True),
        types.StructField('NOM_PARC', types.StringType(), True),
        types.StructField('Rue_de', types.StringType(), True),
        types.StructField('Rue_a', types.StringType(), True),
        types.StructField('Distance_pave', types.StringType(), True),
        types.StructField('Distance_ligne_rue', types.StringType(), True),
        types.StructField('Stationnement_jour', types.StringType(), True),
        types.StructField('Stationnement_heure', types.StringType(), True),
        types.StructField('District', types.StringType(), True),
        types.StructField('Arbre_remarquable', types.StringType(), True),
        types.StructField('Code_secteur', types.StringType(), True),
        types.StructField('Nom_secteur', types.StringType(), True),
        types.StructField('Coord_X', types.DoubleType(), True),
        types.StructField('Coord_Y', types.DoubleType(), True),
        types.StructField('Longitude', types.DoubleType(), True),
        types.StructField('Latitude', types.DoubleType(), True)])




        df = spark.read \
            .option("header", "true") \
            .csv(
                '/opt/airflow/data/arbres-publics.csv',
                schema=public_tree_schema,
                timestampFormat="yyyy-MM-dd'T'HH:mm:ss"
            )




        from pyspark.sql import functions as F




        df_filtered_data_plantation = df.filter(
            (F.col("Date_Plantation") >= F.to_timestamp(F.lit("1900-01-01T00:00:00Z"))) | F.col("Date_Plantation").isNull()
        )




        df_filtered_date_releve = df_filtered_data_plantation.filter(
            (F.col("Date_Releve") >= F.to_timestamp(F.lit("1900-01-01T00:00:00Z"))) | F.col("Date_Releve").isNull()
        )

        logger.info(f"Writing to dataframe to bucket.")
        


        df_filtered_date_releve.repartition(4)\
        .write.parquet('gs://dtc_data_lake_de_nytaxi_mee/pq/montreal_trees/', mode="overwrite")

        print("count: ", df_filtered_date_releve.count())

        spark.stop()
    except exception as e:
        logger.error(f"Error during Spark job execution: {e}")
        raise
    finally:
        logger.info(f"Cleaning up temporary keyfile: {keyfile_path}")
        os.remove(keyfile_path)
