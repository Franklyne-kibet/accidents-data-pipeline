from pathlib import Path
import pandas as pd

from prefect import flow,task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(log_prints=True)
def extract_from_gcs() -> Path:
    """Download data from GCS"""
    gcs_path = f"data/us_accidents_2016-2021.parquet"
    gcs_block = GcsBucket.load("project-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path = f"../")
    return Path(f"../{gcs_path}")

@task(log_prints=True)
def check_data(path: Path) -> pd.DataFrame:
    """Check Data"""
    df = pd.read_parquet(path)
    print(f"columns:{df.dtypes}")
    print(f"rows:{len(df)}")
    
    return df

@task(log_prints=True)
def write_bq(df: pd.DataFrame) -> None:
    """Write data to BigQuery"""
    gcp_credentials_block = GcpCredentials.load("project-credentials")

    df.to_gbq(
        destination_table="accidents_data_all.accidents",
        project_id="de-project-franklyne",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500000,
        if_exists="append",
    )

@flow()
def etl_gcs_to_bq():
    path = extract_from_gcs()
    data = check_data(path)
    write_bq(data)
    
if __name__ == '__main__':
    etl_gcs_to_bq()