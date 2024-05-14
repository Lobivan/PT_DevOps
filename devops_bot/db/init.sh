#!/bin/bash

CONFIG_FILE_DB=`psql -U postgres --no-align --quiet --tuples-only --command='SHOW config_file'`

sed -i "s/^#*\(archive_mode *= *\).*/\1on/" $CONFIG_FILE_DB
sed -i "s|^#*\(archive_command *= *\).*|\1'cp %p /oracle/pg_data/archive/%f'|" $CONFIG_FILE_DB
sed -i "s/^#*\(max_wal_senders *= *\).*/\110/" $CONFIG_FILE_DB
sed -i "s/^#*\(wal_level *= *\).*/\1replica/" $CONFIG_FILE_DB
sed -i "s/^#*\(wal_log_hints *= *\).*/\1on/" $CONFIG_FILE_DB
sed -i "s/^#*\(log_replication_commands *= *\).*/\1on/" $CONFIG_FILE_DB
sed -i "s/^#*\(logging_collector *= *\).*/\1on/" $CONFIG_FILE_DB

HBA_FILE_DB=`psql -U postgres --no-align --quiet --tuples-only --command='SHOW hba_file'`

echo "host all all 0.0.0.0/0 trust" >> $HBA_FILE_DB
echo "host replication $DB_REPL_USER 0.0.0.0/0 trust" >> $HBA_FILE_DB

psql -c "CREATE USER $DB_REPL_USER WITH REPLICATION LOGIN PASSWORD '$DB_REPL_PASSWORD';"
psql -c "CREATE DATABASE $DB_DATABASE;"
psql -d $DB_DATABASE -a -f /init.sql
psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_DATABASE TO $DB_USER;"
psql -d $DB_DATABASE -c "ALTER TABLE email OWNER TO $DB_USER;"
psql -d $DB_DATABASE -c "ALTER TABLE phones OWNER TO $DB_USER;"

#DB_BIN_PATH=`pg_config --bindir`
#DB_DATA_PATH=`psql -U postgres --no-align --quiet --tuples-only --command='SHOW data_directory'`
#/$DB_BIN_PATH/pg_ctl restart -D $DB_DATA_PATH