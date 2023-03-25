# Workflow Orchestration

## Prefect

Prefect is used in this project as workflow orchestration tool in creating ETL workflows to `extract`, `transform`, and `load` data.

I will use Postgres and GCP's Google Cloud Storage and BigQuery.

## Setup

Clone the repo locally

### install packages

In a conda environment, install all package dependencies with

```Python
pip install -r requirements.txt
```

### Start the Prefect Orion server locally

```python
prefect orion start
```

### Set up GCP

- Log in to [GCP](<https://cloud.google.com/>)
- Create a Project
- Set up Cloud Storage
- Set up BigQuery
- Create a service account with the required policies to interact with both services

### Register the block types that come with prefect-gcp

```python
prefect block register -m prefect_gcp
```

### Create Prefect GCP blocks

1) Create a GCP Credentials block in the UI.

   - Paste your service account information from your JSON file into the Service Account Info block's field.

2) Create a GCS Bucket block in UI

   - Alternatively, create these blocks using code by following the templates in the blocks folder.

### Create flow code

Write your Python functions and add `@flow` and `@task` decorators.

**Note:** all code should be run from the top level of your folder to keep file paths consistent.

### Create deployments

Prefect deployment code is available in deployment folder [here](./deployments/deployment_flow.py)

#### Prefect Deployment

To build a prefect deployment run the command below at the top level of your deployment folder.

 ```python
   # prefect deployment build (creates a yaml file)
   prefect deployment build deployments/deployment_flow.py:etl_parent_flow -n "Pyspark-ETL"
   # Apply changes
   prefect deployment apply etl_parent_flow-deployment.yaml
   # Start prefect agent
   prefect agent start  --work-queue "default"  
 ```

#### Scheduling deployment using cron tab

This will schedule the deployment to be executed at 5:00 AM on the first day of every month.

```python
   prefect deployment build deployments/deployment_flow.py:etl_parent_flow -n "Pyspark-ETL" --cron "0 5 1 * *" -a    
```
