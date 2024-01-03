# Basierend auf dem offiziellen Postgres-Image
FROM postgres:latest

# Umgebungsvariablen für das automatische Ausführen der Skripte setzen
ENV POSTGRES_DB=movies
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword

# Kopieren der SQL-Skripte in das Docker-Image
COPY createDB.sql /docker-entrypoint-initdb.d/10-createDB.sql
COPY insertDB.sql /docker-entrypoint-initdb.d/20-insertDB.sql

# Der Standard-Port für PostgreSQL ist 5432
EXPOSE 5432/tcp