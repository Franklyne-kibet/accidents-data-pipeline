## How to run dbt project

### Creating the project

Create an empty github repository and connect it to dbt cloud.

Start the project by running `$ dbt init`)

Create a branch and checkout the branch to be able to read/write the project.

Try running the following commands:

- `dbt run`
- `dbt test`

### dbt files

- [stg_accidents_data](models/staging/stg_accidents_data.sql) file stages data from the bigquery dataset. This is where data is transformed and creates a view in bigquery dataset.
- [fact_accidents](models/core/fact_accidents.sql) file creates a table of transformed data in bigquery dataset.
- [get_accident_severity](macros/get_accident_severity.sql) file is a macro that receives accident severity and returns the corresponding description.
- [dbt_project](dbt_project.yml) file used to configure the dbt project.
- [packages](packages.yml) file installs project dependencies.

Lineage graph of dbt process:
![lineage graph](../../resources/images/lineage/lineage%20graph.png)

### Workflow

![workflow](../../resources/images/architecture/workflow.jpg)

### Execution

We are runnning the project in dbt cloud:

1) Create a Production Environment and configure it accordingly.

2) Create and Execute job this will run dbt models and create a view and table in bigquery dataset.

3) The dbt job will execute commands `$ dbt run` and `$ dbt test` is used to run dbt models and output the results to bigquery.

4) View the documentation for the project, after the job is completed successfully in the cloud.

5) The output of our models is stored in production dataset in bigquery .
