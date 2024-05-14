FROM postgres:15
RUN apt-get update

COPY ./init.sh /docker-entrypoint-initdb.d/init.sh
RUN chmod +x /docker-entrypoint-initdb.d/init.sh
COPY ./init.sql ./init.sql

RUN mkdir -p /oracle/pg_data/archive/
RUN chown postgres:postgres /oracle/pg_data/archive/

# CMD [ "pg_ctl -D /var/lib/postgresql/data -l logfile start" ]