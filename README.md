# US-Accidents: A Countrywide Traffic Accident Dataset

## Overview

The US-Accidents: A Countrywide Traffic Accident Dataset is a comprehensive dataset that contains detailed information about traffic accidents that occurred in the United States from February 2016 to December 2021. The dataset was compiled by ZenDrive, a data analytics firm, using a variety of sources such as traffic cameras, traffic sensors, and user reports from mobile apps.

## Project Description

- The aim of this project, is to perform Extract, Transform, Load, on US-Accidents dataset, to answer questions such as :

  - Identifying high-risk areas for traffic accidents and developing targeted interventions to improve safety.
  - Analyzing the impact of weather conditions on traffic accidents.
  - Studying accident hotspot locations

## Purpose

The purpose of this project is to provide a large and comprehensive dataset for researchers and practitioners in fields such as transportation engineering, public safety, and data science to analyze traffic accident patterns and develop strategies for reducing the number and severity of accidents on US roads.

## Dataset Details

The dataset contains over 2.8 million records, making it one of the largest publicly available traffic accident datasets. Each record includes information such as the location of the accident, the severity of the accident, the weather conditions at the time of the accident, and more. The dataset is hosted on Kaggle, a popular platform for hosting and sharing data science projects, and can be downloaded for free.

## Potential Use Cases

Some potential use cases for the US-Accidents: A Countrywide Traffic Accident Dataset include:

- Developing machine learning models to predict the severity of traffic accidents based on various factors.
- Studying the effectiveness of traffic safety policies and interventions.
- Studying the impact of precipitation or other environmental stimuli on accident occurrence.
- Real-time accident prediction.
  
Overall, the US-Accidents: A Countrywide Traffic Accident Dataset is a valuable resource for anyone interested in understanding and improving traffic safety in the United States.

## Architecture

---

The technical architecture for this project is as show below:
![architecture](resources/images/architecture/architecture.jpg)

1) `cd` into the [setup/terraform](./setup/terraform_gcp/terraform/) folder. Using terminal run the following commands to create **gcs storage bucket** and **Bigquery Dataset** .
   - `terraform init`
   - `terraform plan`
   - `terraform apply`

2) Data Extraction is done using Kaggle API.
  Set up an VM instance in Google cloud. Then, run `pip install kaggle`.

3) Run the ETL pipeline, scheduled using Prefect. Data processing is done using Spark and Data is finally ingested into Google Cloud Storage and Google BigQuery.

4) Data building is done using Data Building Tool (dbt). Visit the [analytics_engineering](./analytics_engineering/dbt_accidents/) folder for detailed information.

## ETL Pipeline
