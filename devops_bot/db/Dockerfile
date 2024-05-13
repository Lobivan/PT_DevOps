FROM postgres:15
RUN apt-get update

COPY ./init.sql /docker-entrypoint-initdb.d/init.sql.raw

RUN mkdir -p /oracle/pg_data/archive/
RUN chown postgres:postgres /oracle/pg_data/archive/

CMD [ "pg_ctl -D /var/lib/postgresql/data -l logfile start" ]