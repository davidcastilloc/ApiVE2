FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10
RUN apk add --no-cache \
    gcc g++ libxslt-dev \
    libffi-dev libressl-dev \
    libxml2-dev zlib-dev \
    &&/usr/local/bin/python -m pip install Scrapy~=2.4.1 
COPY ./src/app /app
