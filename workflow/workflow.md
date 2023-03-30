# Workflow Orchestration

## Prefect

Prefect is used in this project as workflow orchestration tool in creating ETL workflows to `extract`, `transform`, and `load` data.

I will use GCP's Google Cloud Storage as data lake and BigQuery as data warehouse.

## Setup

Clone the repo

### Start the Prefect Orion server locally

```python
prefect orion start
```

### Flow code

The flow code uses `@flow` & `@task` decorators.

> **Note:** all code should be run from the top level of your folder to keep file paths consistent.

#### Prefect Deployment

To build a prefect deployment run the command below at the top level of your deployment folder.

 ```python
   # prefect deployment build (creates a yaml file)
   prefect deployment build pyspark/etl_api_gcs_bq.py:etl_api_gcs_bq -n "Pyspark-ETL"
   # Apply changes
   prefect deployment apply etl_api_gcs_bq-deployment.yaml
   # Start prefect agent
   prefect agent start  --work-queue "default"  
 ```

#### Scheduling deployment using cron tab

This will schedule the deployment to be executed at 5:00 AM on the first day of every month.

```python
   prefect deployment build pyspark/etl_api_gcs_bq.py:etl_api_gcs_bq -n "Pyspark-ETL" --cron "0 5 1 * *" -a    
```
