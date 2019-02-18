#!/bin/bash

mkdir -p $HOME/docker/volumes/postgres
docker build -t app/reportatron .
docker run --rm --network host -d -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data app/reportatron
