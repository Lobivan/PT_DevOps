FROM postgres:15
COPY ./init.sh /docker-entrypoint-initdb.d/init.sh
COPY ./init.sql ./init.sql
RUN chmod +x /docker-entrypoint-initdb.d/init.sh


RUN mkdir -p /oracle/pg_data/archive/
RUN chown postgres:postgres /oracle/pg_data/archive/

# CMD [ "pg_ctl -D /var/lib/postgresql/data -l logfile start" ]