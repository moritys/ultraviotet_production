FROM python:3.11

RUN mkdir /app

COPY requirements.txt /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && python3 -m pip install pip --upgrade \
    && apt-get -y install build-dep python-psycopg2 python3-dev libpq5 \
    && pip3 install -r /app/requirements.txt --no-cache-dir

COPY uv_prod/ /app

WORKDIR /app

CMD ["gunicorn", "uv_prod.wsgi:application", "--bind", "0:8000"]