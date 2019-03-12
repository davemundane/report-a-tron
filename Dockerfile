FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y python3 python3-dev python3-pip

RUN apt-get install -y postgresql-10 postgresql-contrib

COPY . /app

WORKDIR /app

EXPOSE 5432

RUN groupadd webapp && \
	usermod -a -G webapp postgres

RUN chown -R postgres:webapp /app

RUN chmod +x /app/startup.sh

USER postgres

ENTRYPOINT ["./startup.sh"]
