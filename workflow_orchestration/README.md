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

Note: all code should be run from the top level of your folder to keep file paths consistent.

### Create deployments

**Docker deployment code** is available in deployment folder

#### Prefect Docker Deployments 

1) Create docker image
   - `docker image build -t franklyne/prefect:zoom .`
   - `docker image push franklyne/prefect:zoom`
   - `docker pull franklyne/prefect:zoom`

2) Prefect docker deployent

   ```python
   python flows/deployments/docker_deploy.py
   ```

3) Interface docker container with orion server

```python
prefect config set PREFECT_API_URL="insert_your_url/api"
```

4) Start prefect agent

```python
prefect agent start -q default
```

5) Run flow (runs in docker container)

```python
prefect deployment run etl_web_to_gcs/docker-flow
```