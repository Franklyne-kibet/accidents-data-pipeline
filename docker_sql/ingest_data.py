import os
import argparse


from time import time

import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    #url = params.url
    
    # Set the dataset and file paths
    csv_name = 'us-accidents.zip'
    
    dataset_name = 'sobhanmoosavi/us-accidents'
    os.system(f'kaggle datasets download -d {dataset_name}')
    #os.system(f'unzip {dataset_name}.zip')
    #os.system(f'rm {dataset_name}.zip')
    
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    
    df = next(df_iter)
    
    df.Start_Time = pd.to_datetime(df.Start_Time)
    df.End_Time = pd.to_datetime(df.End_Time)
    df.Weather_Timestamp = pd.to_datetime(df.Weather_Timestamp)
    
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    
    while True:
        try:
            t_start = time()
        
            df = next(df_iter)
            
            df.Start_Time = pd.to_datetime(df.Start_Time)
            df.End_Time = pd.to_datetime(df.End_Time)
            df.Weather_Timestamp = pd.to_datetime(df.Weather_Timestamp)
            
            df.to_sql(name=table_name, con=engine, if_exists='append')
            
            t_end = time()
            
            print("inserted another chunk...., took %.3f seconds" %(t_end - t_start))
        except StopIteration:
            print("Finished ingesting data into the database")
            break
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    
    parser.add_argument('--user', required=True, help="user for postgres")
    parser.add_argument('--password', required=True, help="password for postgres")
    parser.add_argument('--host', required=True, help="host for postgres")
    parser.add_argument('--port', required=True, help="port for postgres")
    parser.add_argument('--db', required=True, help="database for postgres")
    parser.add_argument('--table_name', required=True, help="table name for postgres to write data to")
    #parser.add_argument('--url', required=True, help="url for data source")
    
    args = parser.parse_args()
    main(args)