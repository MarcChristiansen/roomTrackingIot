FROM python:buster

WORKDIR /app
ADD data_ingest.py /app/
ADD database/dbClient.py /app/database/
ADD database/sqliteSetup.py /app/database/

ADD requirements.txt /app/
RUN pip3 install -r requirements.txt

CMD [ "python3", "data_ingest.py" ]