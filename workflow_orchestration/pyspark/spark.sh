URL="local[*]"
spark-submit \
    --master="${URL}" \
    --driver-memory 2g \
    pyspark/etl_api_gcs_bq.py