FROM python:3.11-slim-buster

RUN mkdir /app

COPY requirements.txt /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip3 install -r /app/requirements.txt --no-cache-dir

COPY uv_prod/ /app

WORKDIR /app

CMD ["gunicorn", "uv_prod.wsgi:application", "--bind", "0:8000"]