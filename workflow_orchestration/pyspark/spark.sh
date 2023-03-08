#URL="spark://de-project.us-central1-a.c.de-project-franklyne.internal:7077"
URL="spark://192.168.0.12:7077" #Local instance
spark-submit \
    --master="${URL}" \
    spark_sql.py \
        --input_green=data/pq/* \
        --output=data/report-2021

URL="local[*]"
spark-submit \
    --master="${URL}" \
    --driver-memory 2g \
    flows/etl_web_gcs.py