FROM python:3.11-slim

RUN mkdir /app

COPY requirements.txt /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip3 install -r /app/requirements.txt --no-cache-dir

COPY uv_prod/ /app

WORKDIR /app

CMD ["python3", "manage.py", "runserver"]