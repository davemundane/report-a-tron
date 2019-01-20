import psycopg2
import datetime
import os

db_password = os.environ.get('POSTGRES_PASSWORD')

def createNewAsset(asset_name, asset_type, asset_owner, timestamp, asset_notes):

	sql = "INSERT INTO assets(asset_name,asset_type,asset_owner,created_on,asset_notes) VALUES (%s,%s,%s,%s,%s)"
	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=")
		cur = conn.cursor()
		cur.execute(sql, (asset_name, asset_type, asset_owner, timestamp, asset_notes,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def createNewEngagement(asset_id,engform_location,main_contact,risk_rating,received_on,action_taken, eng_notes):

	sqlCreateNewEngagement = "INSERT INTO engagements(asset_id,engform_location,main_contact,risk_rating,received_on,action_taken, eng_notes) VALUES (%s,%s,%s,%s,%s,%s, %s)"
	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlCreateNewEngagement, (asset_id,engform_location,main_contact,risk_rating,received_on,action_taken, eng_notes,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def createNewTest(asset_id,eng_id,test_type,exec_summary,base_location,limitations,main_contact,created_on,test_date,test_notes):

	sqlCreateNewTest = "INSERT INTO tests(asset_id,eng_id,test_type,exec_summary,base_location,limitations,main_contact,created_on,test_date,test_notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlCreateNewTest, (asset_id,eng_id,test_type,exec_summary,base_location,limitations,main_contact,created_on,test_date,test_notes,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def createNewIssue(asset_id,eng_id,test_id,issue_title,issue_location,issue_description,remediation,risk_rating,risk_impact,risk_likelihood,created_on,issue_status,issue_details,issue_notes):

	sqlCreateNewIssue = "INSERT INTO issues(asset_id,eng_id,test_id,issue_title,issue_location,issue_description,remediation,risk_rating,risk_impact,risk_likelihood,created_on,issue_status,issue_details,issue_notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlCreateNewIssue, (asset_id,eng_id,test_id,issue_title,issue_location,issue_description,remediation,risk_rating,risk_impact,risk_likelihood,created_on,issue_status,issue_details,issue_notes,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getAllAssetTableData():

	sql = "SELECT * FROM assets ORDER BY created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getSingleAssetTestData(asset_id):

	sqlTestData = "SELECT * FROM assets WHERE asset_id = %s ORDER BY created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlTestData, (asset_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getEngagementsForAsset(asset_id):

	sqlEngagementData = "SELECT engagements.*, assets.asset_name, assets.asset_id FROM engagements INNER JOIN assets ON engagements.asset_id=assets.asset_id WHERE engagements.asset_id = %s ORDER BY received_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlEngagementData, (asset_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getAllEngagementData():

	sqlEngagementData = "SELECT engagements.*, assets.asset_name, assets.asset_id FROM engagements INNER JOIN assets ON engagements.asset_id=assets.asset_id ORDER BY received_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlEngagementData)
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getTestsForEngagement(eng_id):

	sqlEngagementData = "SELECT tests.*, assets.asset_name, assets.asset_id FROM tests INNER JOIN assets ON tests.asset_id=assets.asset_id WHERE tests.eng_id = %s ORDER BY tests.created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlEngagementData, (eng_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getAllTestData():

	sqlTestData = "SELECT tests.*, assets.asset_name, assets.asset_id FROM tests INNER JOIN assets ON tests.asset_id=assets.asset_id ORDER BY tests.created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlTestData)
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getTestsForAsset(asset_id):

	sqlTestAssetData = "SELECT tests.*, assets.asset_name, assets.asset_id FROM tests INNER JOIN assets ON tests.asset_id=assets.asset_id WHERE tests.asset_id = %s ORDER BY tests.created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlTestAssetData, (asset_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getIssuesForAsset(asset_id):

	sqlIssueAsset = "SELECT assets.asset_id, assets.asset_name, issues.* FROM issues INNER JOIN assets ON issues.asset_id=assets.asset_id WHERE issues.asset_id = %s ORDER BY issues.created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlIssueAsset, (asset_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getIssuesForEngagement(eng_id):

	sqlIssueEng = "SELECT * FROM issues WHERE eng_id = %s ORDER BY created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlIssueEng, (eng_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getIssuesForTest(test_id):

	sqlIssueTest = "SELECT issues.*, assets.asset_name, assets.asset_id FROM issues INNER JOIN assets ON issues.asset_id=assets.asset_id WHERE issues.test_id = %s ORDER BY issues.created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlIssueTest, (test_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getIssuesForAsset(asset_id):

	sqlIssueTest = "SELECT issues.*, assets.asset_name, assets.asset_id FROM issues INNER JOIN assets ON issues.asset_id=assets.asset_id WHERE issues.asset_id = %s ORDER BY issues.created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlIssueTest, (asset_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getAllIssueData():

	sqlIssue = "SELECT issues.*, assets.asset_name, assets.asset_id FROM issues INNER JOIN assets ON issues.asset_id=assets.asset_id ORDER BY issues.created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlIssue)
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def updateSingleIssue(status,issue_id):

	sqlIssueUpdate = "UPDATE issues SET status = %s WHERE issue_id = %s"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlIssueUpdate, (status,issue_id,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getSingleIssue(issue_id):

	sqlSingleIssue = "SELECT * FROM issues WHERE issue_id = %s"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlSingleIssue, (issue_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getTestDataForReport(test_id):

	sqlTestData = "SELECT tests.* from tests INNER JOIN issues ON issues.test_id=tests.test_id WHERE issues.test_id = %s LIMIT 1"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlTestData, (test_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getAssetIdFromTitle(asset_name):

	sqlAssetID = "SELECT asset_id FROM assets WHERE asset_name LIKE %s"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlAssetID, (asset_name,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def countEngagementsForAsset(asset_id):

	sqlCountEng = "SELECT COUNT(eng_id) FROM engagements WHERE asset_id = %s"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlCountEng, (asset_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise


def getIssuesForAssetReport(asset_id, status_open, status_closed, status_RA):

	sqlGetAssetReportIssues = "SELECT * FROM issues WHERE asset_id = %s AND(issue_status LIKE %s OR issue_status LIKE %s OR issue_status LIKE %s)"

	try:
		conn = psycopg2.connect("dbname=reportatron user=postgres password=" + db_password + "")
		cur = conn.cursor()
		cur.execute(sqlGetAssetReportIssues, (asset_id, status_open, status_closed, status_RA,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise
