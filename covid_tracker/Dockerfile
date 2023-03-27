FROM postgres:latest
ENV POSTGRES_DB http_db
COPY migrations/init.sql /docker-entrypoint-initdb.d/