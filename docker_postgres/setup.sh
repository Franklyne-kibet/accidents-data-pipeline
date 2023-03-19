#ingest script
python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5431 \
    --db=us_accidents \
    --table_name=us_accidents_data

docker build -t us_accidents:v001 .
        
#run docker compose
docker-compose up -d