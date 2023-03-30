#!/bin/bash

# initial updates
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install unzip -y

# setup gcloud cli
sudo apt-get install apt-transport-https ca-certificates gnupg -y
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt-get update && sudo apt-get install google-cloud-cli

# anaconda setup
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
# User will need to page down or hit f to get past the MORE prompt
echo -ne "ENTER \n yes \n \n yes \n" | bash Anaconda3-2022.10-Linux-x86_64.sh
rm Anaconda3-2022.10-Linux-x86_64.sh

# terraform
wget https://releases.hashicorp.com/terraform/1.4.2/terraform_1.4.2_linux_amd64.zip
sudo unzip terraform_1.4.2_linux_amd64.zip -d /usr/bin
rm terraform_1.4.2_linux_amd64.zip

# Java
wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz
mkdir spark
tar xzfv openjdk-11.0.2_linux-x64_bin.tar.gz -C spark/
rm openjdk-11.0.2_linux-x64_bin.tar.gz
# export PATH
export JAVA_HOME="${HOME}/spark/jdk-11.0.2"
export PATH="${JAVA_HOME}/bin:${PATH}"

# Spark 
wget https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
tar xzfv spark-3.3.2-bin-hadoop3.tgz -C spark/
rm spark-3.3.2-bin-hadoop3.tgz
# export path
export SPARK_HOME="${HOME}/spark/spark-3.3.2-bin-hadoop3"
export PATH="${SPARK_HOME}/bin:${PATH}"

#Pyspark
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"