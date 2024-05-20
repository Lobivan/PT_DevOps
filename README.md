# PT_DevOps
PT Start Модуль 5 - DevOps
Формат файла секретов:
```
ans_hosts:
  bot:
    host: 192.168.88.240
    user: lobivan
    password: 123
  db:
    host: 192.168.88.240
    user: lobivan
    password: 123
  db_repl: 
    host: 192.168.88.239
    user: lobivan
    password: 123

env:
  TOKEN:
  RM_HOST: 192.168.88.240
  RM_PORT: 22
  RM_USER: lobivan
  RM_PASSWORD: 123
  DB_USER: postgres
  DB_PASSWORD: 123
  DB_PORT: 5432
  DB_DATABASE: ptstartdb
  DB_REPL_USER: repl_user
  DB_REPL_PASSWORD: 123
  DB_REPL_PORT: 5432

other:
  archive_dir: "/oracle/pg_data/archive/"
  pg_version: 14

```