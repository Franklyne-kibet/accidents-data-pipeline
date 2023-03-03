import os
import pandas as pd
from pathlib import Path

from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
from prefect_gcp.cloud_storage import GcsBucket

@task(log_prints=True,tags=['extract'], cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(dataset_name:str) -> pd.DataFrame:
    """Download accidents data from kaggle into pandas DataFrame"""
    csv_name = "data/us-accidents.zip"
    
    os.system(f"kaggle datasets download -d {dataset_name} -p data")
    
    df = pd.read_csv(csv_name)
    
    return df

@task(log_prints=True)
def transform_data(df:pd.DataFrame) -> pd.DataFrame:
    """Fix Dtypes issues"""
    df['Start_Time'] = pd.to_datetime(df['Start_Time']).dt.round('us')
    df['End_Time'] = pd.to_datetime(df['End_Time']).dt.round('us')
    df['Weather_Timestamp'] = pd.to_datetime(df['Weather_Timestamp']).dt.round('us')
    df = df.rename(columns={
        'Distance(mi)': 'Distance_miles',
        'Temperature(F)': 'Temperature_F',
        'Wind_Chill(F)': 'Wind_Chill_F',
        'Humidity(%)': 'Humidity_perc',
        'Pressure(in)': 'Pressure_inches',
        'Visibility(mi)': 'Visibility_miles',
        'Wind_Speed(mph)': 'Wind_Speed_mph',
        'Precipitation(in)': 'Precipitation_inches'
    })
    
    print(f"columns:{df.dtypes}")
    print(f"rows: {len(df)}")
    
    return df

@task(log_prints=True)
def write_local(df:pd.DataFrame, dataset_file:str) -> Path:
    """Write DataFrame out as Parquet file"""
    path = Path(f"data/{dataset_file}.parquet")
    df.to_parquet(path, compression='gzip')
    
    return path

@task(log_prints=True, retries=3)
def upload_to_gcs(path: Path) -> None:
    """Upload local parquet files to GCS"""
    gcs_block = GcsBucket.load("project-gcs")
    path = Path(path).as_posix()
    gcs_block.upload_from_path(
        from_path = path,
        to_path = path,
        timeout = (10,2000)
    )
    return

@flow()
def etl_web_to_gcs():
    """The Main ETL function"""
    dataset_name  = "sobhanmoosavi/us-accidents"
    dataset_file = "us_accidents_2016-2021"
    
    df = extract_data(dataset_name)
    raw_data = transform_data(df)
    local = write_local(raw_data, dataset_file)
    upload_to_gcs(local)

if __name__ == '__main__':
    etl_web_to_gcs()