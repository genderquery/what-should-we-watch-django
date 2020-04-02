#!/bin/bash

openssl req -new -x509 -days 365 -nodes -text -out server.crt \
  -keyout server.key -subj "/CN=localhost"

docker build -t postgres-dev .

rm server.crt server.key

docker run -d --name postgres-dev \
    -p 5432:5432 \
    -e POSTGRES_HOST_AUTH_METHOD=trust \
    postgres-dev \
    -c ssl=on \
    -c ssl_cert_file=/var/lib/postgresql/server.crt \
    -c ssl_key_file=/var/lib/postgresql/server.key

