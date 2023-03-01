FROM python:3.11

COPY docker-requirements.txt .

RUN apt-get install wget
RUN pip install -r docker-requirements.txt --trusted-host pypi.python.org --no-cache-dir

WORKDIR /app

COPY ingest_data.py ingest_data.py
COPY kaggle.json /root/.kaggle/kaggle.json

ENTRYPOINT [ "python", "ingest_data.py" ]