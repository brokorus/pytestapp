FROM python:3.6-alpine

COPY requirements.txt test.py ./
ENV VAULT_ADDR='http://127.0.0.1:8200' \
    DBHOSTNAME='postgresql.svc.cluster.local' \
    DBPASS='admin' \
    DBUSERNAME='postgres' \
    DBNAME='test' \
    DBPORT='8081' \
    DBTABLE='person' 

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    pip install psycopg2 && \
		env && \
    pip install -r requirements.txt 

#CMD ["python3", "/test.py"]
CMD ["sh"]
