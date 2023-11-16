FROM python:3

ENV PYTHONUNBUFFERED 1

COPY . .

RUN apt-get update && apt-get dist-upgrade -y
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 manage.py makemigrations && python3 manage.py migrate 

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]

EXPOSE 8000
