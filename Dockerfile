FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /root

COPY <<EOF .pg_service.conf
[project_service]
host=172.28.5.0
user=root
dbname=project
port=5432
EOF

WORKDIR /app

COPY <<EOF .project_pgpass
172.28.5.0:5432:project:root:test
EOF

RUN chmod 600 .project_pgpass

RUN apt-get update && apt-get dist-upgrade -y

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
