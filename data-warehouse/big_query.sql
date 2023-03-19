-- Creating External Table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `de-project-franklyne.accidents_data_all.external_accidents_data`
OPTIONS
(
  format = 'parquet',
  uris  = [
    'gs://accidents_data_lake/data/*'
  ]
);

-- CREATE A TABLE
CREATE OR REPLACE TABLE `de-project-franklyne.accidents_data_all.accidents_data`
AS
SELECT * FROM `de-project-franklyne.accidents_data_all.external_accidents_data`;

-- Count for number of accidents from accidents_data table
SELECT COUNT(*) FROM `de-project-franklyne.accidents_data_all.accidents_data`;

-- Create a Non-Partitioned table from external table
CREATE OR REPLACE TABLE `de-project-franklyne.accidents_data_all.accidents_data_non_partitioned`
AS
SELECT *FROM `de-project-franklyne.accidents_data_all.external_accidents_data`;

-- Create a Partitioned Table from External Table
CREATE OR REPLACE TABLE `de-project-franklyne.accidents_data_all.accidents_data_partitioned`
PARTITION BY 
  DATE(Start_Time) AS
SELECT * FROM `de-project-franklyne.accidents_data_all.external_accidents_data`;

-- Impact of partition
-- Scanning ~ 50.5MB of data
SELECT DISTINCT(ID)
FROM `de-project-franklyne.accidents_data_all.accidents_data_non_partitioned` 
WHERE DATE(Start_Time) BETWEEN '2016-02-08' AND '2017-02-08';

-- Scanning ~ 2.35Mb of data
SELECT DISTINCT(ID)
FROM `de-project-franklyne.accidents_data_all.accidents_data_partitioned` 
WHERE DATE(Start_Time) BETWEEN '2016-02-08' AND '2017-02-08';

-- Partition Information
SELECT table_name, partition_id, total_rows
FROM `accidents_data_all.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'accidents_data_partitioned'
ORDER BY total_rows DESC

-- Creating a partition and cluster table
CREATE OR REPLACE TABLE `de-project-franklyne.accidents_data_all. accidents_data_partitioned_clustered`
PARTITION BY DATE(Start_Time)
CLUSTER BY Severity AS
SELECT * FROM `de-project-franklyne.accidents_data_all.external_accidents_data`

-- Query Scans 4.65Mb
SELECT COUNT(*) AS accidents
FROM `de-project-franklyne.accidents_data_all.accidents_data_partitioned`
WHERE DATE(Start_Time) BETWEEN '2016-02-08' AND '2018-02-08'
AND Severity = 1

-- Query Scans 2.32Mb
SELECT COUNT(*) AS accidents
FROM `de-project-franklyne.accidents_data_all.accidents_data_partitioned_clustered`
WHERE DATE(Start_Time) BETWEEN '2016-02-08' AND '2018-02-08'
AND Severity = 1