-- Create a Non-Partitioned table from external table
CREATE OR REPLACE TABLE `de-project-franklyne.production.accidents_data_non_partitioned`
AS
SELECT * FROM `de-project-franklyne.production.fact_accidents`;

-- Create a Partitioned table from production table
CREATE OR REPLACE TABLE `de-project-franklyne.production.accidents_data_partitioned`
PARTITION BY
    Date(Start_Time) AS
SELECT * FROM `de-project-franklyne.production.fact_accidents`;

-- Impact of partition
-- Scanning ~ 50.5MB of data
SELECT DISTINCT(Id)
FROM `de-project-franklyne.production.accidents_data_non_partitioned`
WHERE DATE(Start_Time) BETWEEN '2016-02-08' AND '2017-02-08';

-- Scanning ~ 2.35Mb of data
SELECT DISTINCT(Id)
FROM `de-project-franklyne.production.accidents_data_partitioned`
WHERE DATE(Start_Time) BETWEEN '2016-02-08' AND '2017-02-08';

-- Creating a partition and cluster table
CREATE OR REPLACE TABLE `de-project-franklyne.production.accidents_data_partitioned_clustered`
PARTITION BY DATE(Start_Time)
CLUSTER BY Severity AS
SELECT * FROM `de-project-franklyne.production.fact_accidents`

-- Query Scans 4.65Mb
SELECT COUNT(*) AS accidents
FROM `de-project-franklyne.production.accidents_data_partitioned`
WHERE DATE(Start_Time) BETWEEN '2016-02-08' AND '2018-02-08'
AND Severity = 1

-- Query Scans 2.32Mb
SELECT COUNT(*) AS accidents
FROM `de-project-franklyne.production.accidents_data_partitioned_clustered`
WHERE DATE(Start_Time) BETWEEN '2016-02-08' AND '2018-02-08'
AND Severity = 1