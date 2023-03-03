import os
import pandas as pd

from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
from prefect_sqlalchemy import SqlAlchemyConnector

@task(log_prints=True, tags=['extract'],cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(dataset_name:str):
    """Download accidents data from kaggle into pandas DataFrame"""
    csv_name = 'data/us-accidents.zip'
    
    os.system(f'kaggle datasets download -d {dataset_name} -p data')
    
    df = pd.read_csv(csv_name)
    
    return df

@task(log_prints=True)
def transform_data(df):
    """Fix dtype issues"""
    df['Start_Time'] = pd.to_datetime(df['Start_Time'])
    df['End_Time'] = pd.to_datetime(df['End_Time'])
    df['Weather_Timestamp'] = pd.to_datetime(df['Weather_Timestamp'])
    
    print(df.head(2))
    print(f"columns:{df.dtypes}")
    print(f"rows:{len(df)}")
    
    return df

@task(log_prints=True, retries=3)
def load_data(table_name, df):
    """Load data to Postgres database"""
    connection_block = SqlAlchemyConnector.load("postgres-connector")
    with connection_block.get_connection(begin=False) as engine: 
        chunksize = 100000       
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
        for i, chunk in enumerate(df.groupby(df.index // chunksize)):
            print(f"Inserting chunk {i+1} of {len(df)//chunksize+1}")
            chunk[1].to_sql(name=table_name, con=engine, if_exists='append', index=False)
            print(f"Inserted {len(chunk[1])} rows into {table_name} table")

@flow()
def main_flow(table_name:str="us_accidents_data"):
    """Parent flow"""
    dataset_name = "sobhanmoosavi/us-accidents"
    raw_data = extract_data(dataset_name)
    data = transform_data(raw_data)
    load_data(table_name, data)

if __name__ == "__main__":
    main_flow(table_name="us_accidents_data")  