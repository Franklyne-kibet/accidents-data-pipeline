#Windows
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="us_accidents" \
    -v c:/Users/User/Documents/data-projects/de-zoomcamp-project/docker_sql/accidents_postgres_data:/var/lib/postgresql/data \
    -p 5431:5432 \
postgres:13

#Create docker network
docker network create pg-network

docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="us_accidents" \
    -v c:/Users/User/Documents/data-projects/de-zoomcamp-project/docker_sql/accidents_postgres_data:/var/lib/postgresql/data \
    -p 5431:5432 \
    --network=pg-network \
    --name pg-database \
postgres:13

#pgAdmin for Network
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8081:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4  

#ingest script
python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5431 \
    --db=us_accidents \
    --table_name=us_accidents_data

docker build -t us_accidents:v001 .

# Run on pg-database network
docker run -it \
    --network=pg-network \
    us_accidents:v001 \
        --user=root \
        --password=root \
        --host=pg-database \
        --port=5431 \
        --db=us_accidents \
        --table_name=us_accidents_data
        
#run docker compose
docker-compose up -d