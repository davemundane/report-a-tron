# report-a-tron

Its a simple web app with postgresql database for managing security testing

Create an asset, add engagements to the asset, add tests to the engagements

Store issues against assets, tests and engagements

Write reports for tests etc


## Usage

Clone the repo

Recommended python 3.6+
Works best in a virtualenv or venv 
Use pip to install the requirements
```
pip install -r requirements.txt
```

Install Postgresql

You'll need to edit the files setupdb, createTestData, cleanDatabase and dbstuff to include your postgresql credentials 

To setup the database 
```
python setupdb.py
```
If you want to create some dummy data to play with
```
python createTestData.py
```

