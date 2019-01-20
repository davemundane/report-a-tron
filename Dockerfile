FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3 python3-dev python3-pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --no-binary :all: psycopg2

RUN pip3 install -r requirements.txt

COPY . /app

RUN python3 setupdb.py

ENTRYPOINT [ "python3" ]

CMD [ "report-server.py" ]