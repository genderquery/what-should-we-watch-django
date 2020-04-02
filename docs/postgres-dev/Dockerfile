FROM postgres:12-alpine

COPY server.key /var/lib/postgresql/server.key
COPY server.crt /var/lib/postgresql/server.crt

RUN chmod 600 /var/lib/postgresql/server.key
RUN chown postgres:postgres /var/lib/postgresql/server.key