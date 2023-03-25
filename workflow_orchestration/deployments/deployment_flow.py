import os
import pandas as pd

import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types

from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta


@task(name="Extract Data From Web", log_prints=True, tags=['extract'])
def extract_data(dataset_name:str):
# Set the dataset and file paths
    csv_file = 'data/us-accidents.zip'

    dataset_name = 'sobhanmoosavi/us-accidents'
    os.system(f'kaggle datasets download -d {dataset_name} -p data')
    os.system(f'unzip {csv_file} -d data')

    csv_name = 'data/US_Accidents_Dec21_updated.csv'
    return csv_name
        
@task(name="accidents_schema", log_prints=True)
def data_schema():
    accidents_schema = types.StructType([
        types.StructField('ID', types.StringType(), True),
        types.StructField('Severity', types.IntegerType(), True),
        types.StructField('Start_Time', types.TimestampType(), True),
        types.StructField('End_Time', types.TimestampType(), True),
        types.StructField('Start_Lat', types.DoubleType(), True),
        types.StructField('Start_Lng', types.DoubleType(), True),
        types.StructField('End_Lat', types.DoubleType(), True),
        types.StructField('End_Lng', types.DoubleType(), True),
        types.StructField('Distance_miles', types.DoubleType(), True),
        types.StructField('Description', types.StringType(), True),
        types.StructField('Number', types.DoubleType(), True),
        types.StructField('Street', types.StringType(), True),
        types.StructField('Side', types.StringType(), True),
        types.StructField('City', types.StringType(), True),
        types.StructField('County', types.StringType(), True),
        types.StructField('State', types.StringType(), True),
        types.StructField('Zipcode', types.StringType(), True),
        types.StructField('Country', types.StringType(), True),
        types.StructField('Timezone', types.StringType(), True),
        types.StructField('Airport_Code', types.StringType(), True),
        types.StructField('Weather_Timestamp', types.TimestampType(), True),
        types.StructField('Temperature_F', types.DoubleType(), True),
        types.StructField('Wind_Chill_F', types.DoubleType(), True),
        types.StructField('Humidity_perc', types.DoubleType(), True),
        types.StructField('Pressure_inches', types.DoubleType(), True),
        types.StructField('Visibility_miles', types.DoubleType(), True),
        types.StructField('Wind_Direction', types.StringType(), True),
        types.StructField('Wind_Speed_mph', types.DoubleType(), True),
        types.StructField('Precipitation_inches', types.DoubleType(), True),
        types.StructField('Weather_Condition', types.StringType(), True),
        types.StructField('Amenity', types.BooleanType(), True),
        types.StructField('Bump', types.BooleanType(), True),
        types.StructField('Crossing', types.BooleanType(), True),
        types.StructField('Give_Way', types.BooleanType(), True),
        types.StructField('Junction', types.BooleanType(), True),
        types.StructField('No_Exit', types.BooleanType(), True),
        types.StructField('Railway', types.BooleanType(), True),
        types.StructField('Roundabout', types.BooleanType(), True),
        types.StructField('Station', types.BooleanType(), True),
        types.StructField('Stop', types.BooleanType(), True),
        types.StructField('Traffic_Calming', types.BooleanType(), True),
        types.StructField('Traffic_Signal', types.BooleanType(), True),
        types.StructField('Turning_Loop', types.BooleanType(), True),
        types.StructField('Sunrise_Sunset', types.StringType(), True),
        types.StructField('Civil_Twilight', types.StringType(), True),
        types.StructField('Nautical_Twilight', types.StringType(), True),
        types.StructField('Astronomical_Twilight', types.StringType(), True)
    ])
    
    return accidents_schema

@task(name="Data Transformation", log_prints=True)
def transform_data(csv_name: str,accidents_schema:str) -> pd.DataFrame:
    output_path = "data/pq/"
    
    spark = SparkSession.builder \
        .appName('workflow') \
        .getOrCreate()
    
    df_accidents = spark.read \
        .option("header","true") \
        .schema(accidents_schema) \
        .csv(csv_name)

    df_accidents \
        .repartition(24) \
        .write.parquet(output_path, mode='overwrite')
    
    return output_path

@task(name="Write to GCS", log_prints=True)
def upload_to_gcs(output_path:str):
    os.system(f"gsutil -m cp -r {output_path} gs://test_accidents/")

@task(name="Write to BigQuery", log_prints=True)
def upload_to_bq():    
    os.system(f"bq load \
        --source_format=PARQUET \
        de-project-franklyne:accidents_data_all.tests \
        gs://test_accidents/pq/*.parquet ")
       
@flow()
def etl_parent_flow():
    """Main ETL function"""
    dataset_name  = "sobhanmoosavi/us-accidents"
    
    data = extract_data(dataset_name)
    schema = data_schema()
    clean_data = transform_data(data,schema)
    upload_to_gcs(clean_data)
    upload_to_bq()

if __name__  == '__main__':
    etl_parent_flow()