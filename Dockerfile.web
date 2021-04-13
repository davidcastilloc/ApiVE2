FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10
RUN apk add --no-cache \
    gcc g++ libxslt-dev \
    libffi-dev libressl-dev \
    libxml2-dev zlib-dev 
RUN python -m pip install --upgrade pip
RUN apk add musl-dev python3-dev libffi-dev openssl-dev cargo
RUN /usr/local/bin/python -m pip install SQLAlchemy
RUN /usr/local/bin/python -m pip install aiosqlite
RUN /usr/local/bin/python -m pip install databases
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN /usr/local/bin/python -m pip install Scrapy
COPY ./src/app /app
