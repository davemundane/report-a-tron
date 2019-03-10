#!/bin/bash

service postgresql start
pip3 install -r requirements.txt
python3 setupdb.py
#python3 createTestData.py
python3 report-server.py

