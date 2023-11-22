FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get dist-upgrade -y

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python3 manage.py makemigrations && python3 manage.py migrate 

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
