#Windows
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="us_accidents" \
    -v c:/Users/User/Documents/data-projects/de-zoomcamp-project/docker_sql/accidents_postgres_data:/var/lib/postgresql/data \
    -p 5431:5432 \
postgres:13

# Run on pg-database network
URL="https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents"
docker run -it \
    --network=pg-network \
    ingest_data:pg \
        --user=root \
        --password=root \
        --host=pg-database \
        --port=5431 \
        --db=us_accidents \
        --table_name=us_accidents_data
#run docker compose
docker-compose up -d