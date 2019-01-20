import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect("dbname=reportatron user=postgres password=owen")
cur = conn.cursor()
sqlClear = "DROP TABLE riskaccept"
cur.execute(sqlClear)
conn.commit()
sqlClear = "DROP TABLE issues"
cur.execute(sqlClear)
sqlClear = "DROP TABLE tests"
cur.execute(sqlClear)
sqlClear = "DROP TABLE engagements"
cur.execute(sqlClear)
sqlClear = "DROP TABLE assets"
cur.execute(sqlClear)
cur.close()

conn = psycopg2.connect("dbname=postgres user=postgres password=owen")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
sqlClear = "DROP DATABASE reportatron"
cur.execute(sqlClear)
cur.close()