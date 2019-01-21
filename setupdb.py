import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def createTheDatabase():

	conn = psycopg2.connect("dbname=postgres user=postgres password=database_password")
	conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = conn.cursor()

	try:
		cur.execute("CREATE DATABASE reportatron;")
		cur.close()
		print("reportatron database created")
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()

def createTheTables():

	conn = psycopg2.connect("dbname=reportatron user=postgres password=database_password")
	cur = conn.cursor()

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=database_password")
		cur = conn.cursor()
		sqlApp = "CREATE TABLE assets (asset_id serial PRIMARY KEY, asset_name VARCHAR (255) UNIQUE NOT NULL, asset_type VARCHAR (20) NOT NULL, asset_owner VARCHAR (255) NOT NULL, created_on TIMESTAMP NOT NULL, asset_notes TEXT)"
		cur.execute(sqlApp)
		conn.commit()
		cur.close()
		print("asset table created")
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=database_password")
		cur = conn.cursor()
		sqlEng = "CREATE TABLE engagements (eng_id serial NOT NULL, asset_id integer NOT NULL, CONSTRAINT asset_id_fkey FOREIGN KEY (asset_id) REFERENCES assets (asset_id) MATCH SIMPLE, engform_location VARCHAR (255), main_contact VARCHAR (255), risk_rating VARCHAR (10), PRIMARY KEY (eng_id), received_on VARCHAR (20), action_taken TEXT, eng_notes TEXT)"
		cur.execute(sqlEng)
		conn.commit()
		cur.close()
		print("engagements table created")
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=database_password")
		cur = conn.cursor()
		sqlTab = "CREATE TABLE tests (test_id serial NOT NULL, asset_id integer NOT NULL, CONSTRAINT asset_id_fkey FOREIGN KEY (asset_id) REFERENCES assets (asset_id) MATCH SIMPLE, eng_id integer, CONSTRAINT eng_id_fkey FOREIGN KEY (eng_id) REFERENCES engagements (eng_id) MATCH SIMPLE, test_type VARCHAR (255) NOT NULL, exec_summary TEXT, base_location TEXT, limitations TEXT, main_contact VARCHAR (255), PRIMARY KEY (test_id), created_on TIMESTAMP NOT NULL, test_date VARCHAR (20), test_notes TEXT)"
		cur.execute(sqlTab)
		conn.commit()
		cur.close()
		print("tests table created")
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=database_password")
		cur = conn.cursor()
		sqlVuln = "CREATE TABLE issues (issue_id serial NOT NULL, asset_id integer NOT NULL, CONSTRAINT asset_id_fkey FOREIGN KEY (asset_id) REFERENCES assets (asset_id) MATCH SIMPLE, eng_id integer, CONSTRAINT eng_id_fkey FOREIGN KEY (eng_id) REFERENCES engagements (eng_id) MATCH SIMPLE, test_id integer, CONSTRAINT test_id_fkey FOREIGN KEY (test_id) REFERENCES tests (test_id) MATCH SIMPLE, issue_title VARCHAR (255) NOT NULL, issue_location TEXT, issue_description TEXT, remediation TEXT, risk_rating VARCHAR (10), risk_impact VARCHAR (10),  risk_likelihood VARCHAR (10), PRIMARY KEY (issue_id), created_on TIMESTAMP NOT NULL, issue_status VARCHAR (20) NOT NULL, issue_details TEXT, issue_notes TEXT, ra_date_created TIMESTAMP, ra_date_expires TIMESTAMP, ra_owner TEXT, ra_notes TEXT)"
		cur.execute(sqlVuln)
		conn.commit()
		cur.close()
		print("issues table created")
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()

createTheDatabase()
createTheTables()
