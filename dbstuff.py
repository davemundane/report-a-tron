import psycopg2
import datetime
import os

def createNewAsset(asset_name, asset_type, asset_owner, timestamp, asset_notes):

	sql = "INSERT INTO assets(asset_name,asset_type,asset_owner,created_on,asset_notes) VALUES (%s,%s,%s,%s,%s)"
	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sql, (asset_name, asset_type, asset_owner, timestamp, asset_notes,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def createNewEngagement(asset_id,engform_location,main_contact,risk_rating,received_on,action_taken, eng_notes):

	sqlCreateNewEngagement = "INSERT INTO engagements(engform_location,main_contact,risk_rating,received_on,action_taken, eng_notes) VALUES (%s,%s,%s,%s,%s,%s) RETURNING eng_id"
	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlCreateNewEngagement, (engform_location,main_contact,risk_rating,received_on,action_taken, eng_notes,))
		eng_id = cur.fetchall()[0][0]
		conn.commit()
		cur.close()
		if asset_id: 
			createAssetEngLink(asset_id,eng_id)
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise
		
def createAssetEngLink(link_asset_id, link_eng_id): 

	sqlCreateAssetEngLink = "INSERT INTO links(link_asset_id, link_eng_id) VALUES (%s,%s)"
	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlCreateAssetEngLink, (link_asset_id, link_eng_id,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def createNewTest(eng_id,test_type,exec_summary,base_location,limitations,main_contact,created_on,test_date,test_notes):

	sqlCreateNewTest = "INSERT INTO tests(eng_id,test_type,exec_summary,base_location,limitations,main_contact,created_on,test_date,test_notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlCreateNewTest, (eng_id,test_type,exec_summary,base_location,limitations,main_contact,created_on,test_date,test_notes,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def createNewIssue(eng_id,test_id,issue_title,issue_location,issue_description,remediation,risk_rating,risk_impact,risk_likelihood,created_on,issue_status,issue_details,issue_notes):

	sqlCreateNewIssue = "INSERT INTO issues(eng_id,test_id,issue_title,issue_location,issue_description,remediation,risk_rating,risk_impact,risk_likelihood,created_on,issue_status,issue_details,issue_notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlCreateNewIssue, (eng_id,test_id,issue_title,issue_location,issue_description,remediation,risk_rating,risk_impact,risk_likelihood,created_on,issue_status,issue_details,issue_notes,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise
		
	if risk_rating != 'Info': 
		try: 
			conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
			cur = conn.cursor()
			cur.execute("UPDATE issues SET issue_due_date = CASE WHEN risk_rating LIKE 'Critical' THEN created_on + interval '7 days' WHEN risk_rating LIKE 'High' THEN created_on + interval '30 days' WHEN risk_rating LIKE 'Medium' THEN created_on + interval '60 days' WHEN risk_rating LIKE 'Low' THEN created_on + interval '180 days' END")
			conn.commit()
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			cur.close()
			raise

def updateEngagement(eng_id,engform_location,main_contact,risk_rating,received_on,action_taken, eng_notes, eng_status):

	sqlUpdateEngagement = "UPDATE engagements SET engform_location = %s, main_contact = %s, risk_rating = %s, received_on = %s, action_taken = %s, eng_notes = %s, eng_status = %s WHERE eng_id = %s"
	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlUpdateEngagement, (engform_location,main_contact,risk_rating,received_on,action_taken, eng_notes,eng_status, eng_id,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise
		
def getAllAssetTableData():

	sql = "SELECT * FROM assets ORDER BY created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sql)
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise
		
def getSingleEngagement(eng_id):

	sqlSingleEng = "SELECT * FROM engagements WHERE eng_id = %s"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlSingleEng, (eng_id,))
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
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
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

	sqlEngagementData = "SELECT engagements.*, assets.asset_name, assets.asset_id FROM engagements INNER JOIN links ON engagements.eng_id=links.link_eng_id INNER JOIN assets ON assets.asset_id=links.link_asset_id WHERE assets.asset_id = %s ORDER BY received_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
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

	sqlEngagementData = "SELECT DISTINCT on (engagements.eng_id) engagements.*, assets.asset_name, assets.asset_id FROM engagements LEFT JOIN links ON links.link_eng_id=engagements.eng_id LEFT JOIN assets ON links.link_asset_id=assets.asset_id ORDER BY engagements.eng_id DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlEngagementData)
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise
		
def getOpenEngagementData():

	sqlOpenEngagementData = "SELECT DISTINCT on (engagements.eng_id) engagements.*, assets.asset_name, assets.asset_id FROM engagements LEFT JOIN links ON links.link_eng_id=engagements.eng_id LEFT JOIN assets ON links.link_asset_id=assets.asset_id WHERE engagements.eng_status NOT LIKE 'Closed' ORDER BY engagements.eng_id"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlOpenEngagementData)
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getTestsForEngagement(eng_id):

	sqlEngagementData = "SELECT DISTINCT on (tests.test_id) tests.*, assets.asset_name, assets.asset_id FROM tests LEFT JOIN links ON tests.eng_id=links.link_eng_id LEFT JOIN assets ON assets.asset_id=links.link_asset_id WHERE tests.eng_id = %s ORDER BY tests.test_id"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
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

	sqlTestData = "SELECT tests.*, assets.asset_name, assets.asset_id FROM tests LEFT JOIN links on links.link_eng_id=tests.eng_id LEFT JOIN assets ON links.link_asset_id=assets.asset_id ORDER BY tests.created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
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

	sqlTestAssetData = "SELECT tests.*, assets.asset_name, assets.asset_id FROM tests INNER JOIN links ON links.link_eng_id=tests.eng_id INNER JOIN assets ON links.link_asset_id=assets.asset_id WHERE assets.asset_id = %s ORDER BY tests.created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
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

	sqlIssueAsset = "SELECT assets.asset_id, assets.asset_name, issues.* FROM issues LEFT JOIN links ON links.link_eng_id=issues.eng_id LEFT JOIN assets ON links.link_asset_id=assets.asset_id WHERE assets.asset_id = %s ORDER BY issues.created_on DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
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
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
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

	sqlIssueTest = "SELECT DISTINCT on (issues.issue_id) issues.*, assets.asset_name, assets.asset_id FROM issues LEFT JOIN links ON links.link_eng_id=issues.eng_id LEFT JOIN assets ON links.link_asset_id=assets.asset_id WHERE issues.test_id = %s ORDER BY issues.issue_id"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlIssueTest, (test_id,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def getAllIssueData():

	sqlIssue = "SELECT DISTINCT on (issue_id) issues.*, assets.asset_name, assets.asset_id FROM issues LEFT JOIN links ON links.link_eng_id=issues.eng_id LEFT JOIN assets ON links.link_asset_id=assets.asset_id ORDER BY issues.issue_id DESC"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlIssue)
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def updateSingleIssue(issueTitle,riskRating,riskImpact,riskLikelihood,location,issueStatus,description,remediation,issueDetails,issueNotes,issueRADate,issueRAOwner,issueRAExpiry,issueRANotes,issueID):

	if issueRADate != "None": 
		sqlIssueUpdate = "UPDATE issues SET issue_title = %s, risk_rating = %s, risk_impact = %s, risk_likelihood = %s, issue_location = %s, issue_status = %s, issue_description = %s, remediation = %s, issue_details = %s, issue_notes = %s, issue_ra_date = %s, issue_ra_owner = %s, issue_ra_expiry, issue_ra_notes = %s WHERE issue_id = %s"
		try:
			conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
			cur = conn.cursor()
			cur.execute(sqlIssueUpdate, (issueTitle,riskRating,riskImpact,riskLikelihood,location,issueStatus,description,remediation,issueDetails,issueNotes,issueRADate,issueRAOwner,issueRAExpiry,issueRANotes,issueID,))
			conn.commit()
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			cur.close()
			raise
	
	else: 
		sqlIssueUpdate = "UPDATE issues SET issue_title = %s, risk_rating = %s, risk_impact = %s, risk_likelihood = %s, issue_location = %s, issue_status = %s, issue_description = %s, remediation = %s, issue_details = %s, issue_notes = %s, issue_ra_owner = %s, issue_ra_notes = %s WHERE issue_id = %s"
		try:
			conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
			cur = conn.cursor()
			cur.execute(sqlIssueUpdate, (issueTitle,riskRating,riskImpact,riskLikelihood,location,issueStatus,description,remediation,issueDetails,issueNotes,issueRAOwner,issueRANotes,issueID,))
			conn.commit()
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			cur.close()
			raise

def getSingleIssue(issue_id):

	sqlSingleIssue = "SELECT * FROM issues WHERE issue_id = %s"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
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
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
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
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlAssetID, (asset_name,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise
		
def getAssetIdFromSearch(asset_name):

	sqlAssetSearch = "SELECT * FROM assets WHERE asset_name ~* %s"

	try:
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlAssetSearch, (asset_name,))
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
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
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
		conn = psycopg2.connect("dbname=reportatron user=webapp password=<password>")
		cur = conn.cursor()
		cur.execute(sqlGetAssetReportIssues, (asset_id, status_open, status_closed, status_RA,))
		data = cur.fetchall()
		cur.close()
		return data
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

