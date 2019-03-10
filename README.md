# Report-a-Tron

Web application for managing security assessment engagements, tests and issues. 

Its built in Flask, to run on python 3.6+

## General 

Database structure currently has assets as the primary table - intended to be an application, a server(s), or third party relationship or anything you wish to define as an asset.

For any asset, you can create an engagement - something like a project for say, the deployment of the asset in a production environment

You can also create 'orphaned' engagements - a project to do something that might need security assessment, but doesnt have a defined asset.

At a later date, you can add a link between an asset and an engagement, but inserting asset_id and eng_id into the links table. However if you create an engagement in the UI from an asset, the link will be added for you. 

Engagements becomes the top table in a heirarchy. Tests created must have an associated engagement, tests table has a foreign key referencing the eng_id in engagements. 

Similarly issues created must be associated with a test, and an engagement. Issues have a foreign key referencing test_id and eng_id. 

The issue_links table holds relationships between issues and assets. This allows a single issue reported in a test to be linked to multiple assets, or an issue reported for a test that has multiple linked assets to be assigned to a single asset, rather than them all. This was done to cope with workflows where testing or assessment is carried out on multiple assets at the same time. 

Reports can be produced for any test. Currently the asset reports are not finished, but any test can have a report produced in md and html format. 

Bug fix required here.. once a report is produced it appears to be cached so if you click to produce a report for a different test, the UI displays the cached version. In fact the report has been produced correctly and can be found in the /templates folder under the name convert_md.html

Stats needs a bit of work, but you can all the stats you like from the database. 

Risk acceptance stuff needs to be added. Database is configured to handle it, but it needs building in the UI. 

### Some considerations

dates must be entered as yyyy-mm-dd

Risk ratings must be 'Critical', 'High', 'Medium', 'Low' for the stats and other functions to work. Future dev will be to add constraints to the database to limit input to these values. 

Asset types must be 'Application', 'Third Party', 'Other' for stats etc, though any value can be entered. 

#### To run on Ubuntu: 

Clone the repo somewhere sensible
```
git clone https://github.com/realfukinghigh/report-a-tron.git
```
Install python3 (if you dont already have it), also recommended you install venv or virtualenv, best to read the docs for the method of installing all these

Create a virtualenv to run reportatron, change dir to the new virtualenv, activate the virtualenv:
```
python3 -m virtualenv reportatron
cd reportatron
source bin/activate
```
Navigate to your cloned report-a-tron repo and install the python dependencies:
```
cd report-a-tron
pip install -r requirements.txt
```

In a different shell, install postgres, has been tested on v10 and v11
```
sudo apt install postgresql
```
Install the postgres client
```
sudo apt install postgresql-client-common
```
Or review the postgresql docs for installation instructions of other versions

Depending on how you intend to run the app, you may need to edit postgres config to allow the web app to connect to postgres. 
Edit the file
```
nano /etc/postgresql/10/main/pg_hba.conf
```
Include an additional line 
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   reportatron     webapp                         		md5
```
This is to allow the user 'webapp' to authenticate to postgres database 'reportatron' with a password, rather than unix peer authentication. 
If you intend to edit the users and connection methods, you may need to change these to match your setup.

Restart the postgresql service
```
sudo service postgresql restart
```

#### Configure the database

Connect to the database with user postgres
```
sudo -u postgres psql
```
Create a database, a user and grant the user privileges on the database
```
CREATE DATABASE reportatron;
CREATE USER webapp WITH ENCRYTPED PASSWORD 'reportatron';
GRANT ALL PRIVILEGES ON DATABASE reportatron TO webapp;
```
### N.B. Granting all privileges for the webapp user is not strictly necessary, for production deployments you should consider granting only the privileges required (SELECT, INSERT, UPDATE, CREATE, CONNECT). 
### Currently the scripts used to run the app have hardcoded passwords, for production deployments, change the passwords and consider using a config file containing the creds, stored encrypted which can be accessed by the script when required. Alternatively, edit the app to request passwords at runtime, so they are available in memory only and input by the user starting the app. 

Now create the required tables in the database reportatron, go back to the python virtualenv shell:
```
python setupdb.py
```
Everything should be ready to go, run the app: 
```
python report-server.py
```

### Future work
Currently issue_links table stores links between the asset_id and the issue_id, mainly for reporting purposes. I need to add a web page allowing these to be updated as currently they need to be added directly in the database.

Get docker working properly

Configure auto backups in docker and via scripts

A few changes required to configure database calls to return JSON only - currently most do, not all

Some fixes required on dbstuff.py - it works but its ugly




