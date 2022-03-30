FROM postgres
# ENV POSTGRES_PASSWORD sgn
# ENV POSTGRES_DB sgndb 
EXPOSE 5432
COPY init.sql /docker-entrypoint-initdb.d/
# FROM postgres 
# ENV POSTGRES_PASSWORD postgres 
# ENV POSTGRES_DB testdb 
