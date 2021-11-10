# syntax=docker/dockerfile:1
FROM python:buster

WORKDIR /app
ADD server.py /app/
ADD database/dbClient.py /app/database/
ADD database/sqliteSetup.py /app/database/
ADD static /app/static
ADD templates /app/templates

ADD requirements.txt /app/
RUN pip3 install -r requirements.txt

RUN python3 database/sqliteSetup.py

EXPOSE 80

CMD [ "python3", "server.py" ]