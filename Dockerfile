FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN apk add gcc
RUN apk add g++
RUN apk add libxslt-dev
RUN apk add libffi-dev
RUN apk add libressl-dev
RUN apk add libxml2-dev
RUN apk add zlib-dev
RUN /usr/local/bin/python -m pip install Scrapy~=2.4.1