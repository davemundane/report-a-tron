import psycopg2
import datetime
import random
import time

def createNewAsset(asset_name, asset_type, asset_owner, timestamp, asset_notes):
	
	sql = "INSERT INTO assets(asset_name,asset_type,asset_owner,created_on, asset_notes) VALUES (%s,%s,%s,%s,%s)"
	try: 
		conn = psycopg2.connect("dbname=reportatron user=postgres password=<password>")
		cur = conn.cursor()
		cur.execute(sql, (asset_name, asset_type, asset_owner, timestamp, asset_notes,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		pass
		
def createNewEngagement(asset_id,engform_location,main_contact,risk_rating,received_on,action_taken, eng_notes):

	sqlCreateNewEngagement = "INSERT INTO engagements(asset_id,engform_location,main_contact,risk_rating,received_on,action_taken, eng_notes) VALUES (%s,%s,%s,%s,%s,%s, %s)"
	try: 
		conn = psycopg2.connect("dbname=reportatron user=postgres password=<password>")
		cur = conn.cursor()
		cur.execute(sqlCreateNewEngagement, (asset_id,engform_location,main_contact,risk_rating,received_on,action_taken,eng_notes,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		pass
		
def createNewTest(asset_id,eng_id,test_type,exec_summary,base_location,limitations,main_contact,created_on,test_date,test_notes):

	sqlCreateNewTest = "INSERT INTO tests(asset_id,eng_id,test_type,exec_summary,base_location,limitations,main_contact,created_on,test_date,test_notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	try: 
		conn = psycopg2.connect("dbname=reportatron user=postgres password=<password>")
		cur = conn.cursor()
		cur.execute(sqlCreateNewTest, (asset_id,eng_id,test_type,exec_summary,base_location,limitations,main_contact,created_on,test_date,test_notes,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		
def createNewIssue(asset_id,eng_id,test_id,issue_title,issue_location,issue_description,remediation,risk_rating,risk_impact,risk_likelihood,created_on,issue_status,issue_details,issue_notes):

	sqlCreateNewTest = "INSERT INTO issues(asset_id,eng_id,test_id,issue_title,issue_location,issue_description,remediation,risk_rating,risk_impact,risk_likelihood,created_on,issue_status,issue_details,issue_notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	try: 
		conn = psycopg2.connect("dbname=reportatron user=postgres password=<password>")
		cur = conn.cursor()
		cur.execute(sqlCreateNewTest, (asset_id,eng_id,test_id,issue_title,issue_location,issue_description,remediation,risk_rating,risk_impact,risk_likelihood,created_on,issue_status,issue_details,issue_notes,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		
def makeSomeData(): 

	for i in range(1,6): 
		timenow = datetime.datetime.now().isoformat().split(".")[0]
		createNewAsset("TestWebsite " + str(i), "Application", "TestOwner " + str(i), timenow, "These are some notes about " + str(i))
	for i in range(1,6): 
		timenow = datetime.datetime.now().isoformat().split(".")[0]
		createNewAsset("TestThirdParty " + str(i), "Third Party", "TestOwner " + str(i), timenow, "These are some notes about " + str(i))
	
	print("Created dummy assets")
		
	for i in range(1,11):	
		ratings = {1: "Critical", 2: "High", 3: "Medium", 4: "Low"}
		if i < 6: 
			createNewEngagement(i,"F://ApplicationFolder//" + str(i) + "//Update","TestProjectManager " + str(i + random.randint(1,10)), ratings[random.randint(1,4)],str(random.randint(1,28)) + "/" + str(random.randint(1,12)) + "/2018","Test email sent to main contact","Project to make some minor changes to the app")
			createNewEngagement(i,"F://ApplicationFolder//" + str(i) + "//Update","TestProjectManager " + str(i + random.randint(1,10)), ratings[random.randint(1,4)],str(random.randint(1,28)) + "/" + str(random.randint(1,12)) + "/2018","Test email sent to main contact","Project to make some minor changes to the app")
		else: 
			createNewEngagement(i,"F://ThirdPartyFolder//" + str(i) + "//Update","TestProjectManager " + str(i + random.randint(1,10)), ratings[random.randint(1,4)],str(random.randint(1,28)) + "/" + str(random.randint(1,12)) + "/2018","Test email sent to main contact","Project to send some data to a third party")
			createNewEngagement(i,"F://ThirdPartyFolder//" + str(i) + "//Update","TestProjectManager " + str(i + random.randint(1,10)), ratings[random.randint(1,4)],str(random.randint(1,28)) + "/" + str(random.randint(1,12)) + "/2018","Test email sent to main contact","Project to send some data to a third party")
	
	print("created some enagements")
	
	conn = psycopg2.connect("dbname=reportatron user=postgres password=<password>")
	cur = conn.cursor()
	cur.execute("SELECT asset_id, eng_id FROM engagements")
	data = cur.fetchall()
	cur.close()
	
	for x in data:
		if x[0] < 6: 
			timenow = datetime.datetime.now().isoformat().split(".")[0]
			types = {1:"Application Security Test", 2:"Application Risk Assessment"}
			createNewTest(x[0],x[1],types[random.randint(1,2)],"This is a test record created by a script","https://TestWebsite" + str(x[0]) + ".com","Some Limitations","TestContact " + str(random.randint(1,12)),timenow,str(random.randint(1,28)) + "/" + str(random.randint(1,12)) + "/2018","Some notes about a test created by a script")
			createNewTest(x[0],x[1],types[random.randint(1,2)],"This is a test record created by a script","https://TestWebsite" + str(x[0]) + ".com","Some Limitations","TestContact " + str(random.randint(1,12)),timenow,str(random.randint(1,28)) + "/" + str(random.randint(1,12)) + "/2018","Some notes about a test created by a script")
		else: 
			timenow = datetime.datetime.now().isoformat().split(".")[0]
			types = {1:"Third Party Security Review", 2:"Full Audit"}
			createNewTest(x[0],x[1],types[random.randint(1,2)],"This is a test record created by a script","https://TestThirdParty" + str(x[0]) + ".com","Some Limitations","TestContact " + str(random.randint(1,12)),timenow,str(random.randint(1,28)) + "/" + str(random.randint(1,12)) + "/2018","Some notes about a test created by a script")
			createNewTest(x[0],x[1],types[random.randint(1,2)],"This is a test record created by a script","https://TestThirdParty" + str(x[0]) + ".com","Some Limitations","TestContact " + str(random.randint(1,12)),timenow,str(random.randint(1,28)) + "/" + str(random.randint(1,12)) + "/2018","Some notes about a test created by a script")
			
	print("created lots of tests")
			
	conn = psycopg2.connect("dbname=reportatron user=postgres password=<password>")
	cur = conn.cursor()
	cur.execute("SELECT asset_id, eng_id, test_id FROM tests")
	data = cur.fetchall()
	cur.close()
	
	for x in data: 
		if x[0] < 6: 
			ratings = {1: "Critical", 2: "High", 3: "Medium", 4: "Low"}
			titles = {1: "SQL Injection", 2: "Cross Site Scripting XSS", 3: "Deserialization Vulnerability", 4: "Cross Site Request Forgery CSRF", 5: "Sensitive Data Exposure"}
			statuses = {1: "Open", 2: "Closed", 3: "Risk Accepted"}
			for i in range(3):
				createNewIssue(x[0],x[1],x[2],titles[random.randint(1,5)],"https://TestWebsite" + str(x[0]) + "/vulnfunction.com","This is a test description for an issue created by the setup script","These are the sample remediation steps required to fix the issue created by the script",ratings[random.randint(1,4)],ratings[random.randint(1,4)],ratings[random.randint(1,4)],timenow,statuses[random.randint(1,3)], "These are the notes that accompany the issue created by the script")
		else: 
			ratings = {1: "Critical", 2: "High", 3: "Medium", 4: "Low"}
			titles = {1: "Lack of Encryption At Rest", 2: "Limited Employee Vetting", 3: "Limited Log Monitoring", 4: "Lack of Server Hardening", 5: "Segregation Of Duties"}
			statuses = {1: "Open", 2: "Closed", 3: "Risk Accepted"}
			for i in range(3):
				createNewIssue(x[0],x[1],x[2],titles[random.randint(1,5)],"https://TestThirdParty" + str(x[0]) + "/headquarters.com","This is a test description for an issue created by the setup script","These are the sample remediation steps required to fix the issue created by the script",ratings[random.randint(1,4)],ratings[random.randint(1,4)],ratings[random.randint(1,4)],timenow,"Open", "These are the notes that accompany the issue created by the script")
	
	print("created loads of issues")
		
makeSomeData()


"""	
	for x in range(1,11):
		for y in range(1,21):
			if y % 2 == 0: 
				continue
			elif x < 6: 
				timenow = datetime.datetime.now().isoformat().split(".")[0]
				types = {1:"Application Security Test", 2:"Application Risk Assessment"}
				createNewTest(x,y,types[random.randint(1,2)],"This is a test record created by a script","https://TestWebsite" + str(x) + ".com","Some Limitations","TestContact " + str(y),timenow,str(random.randint(1,28)) + "/" + str(random.randint(1,12)) + "/2018","Some notes about a test created by a script")
			else: 
				timenow = datetime.datetime.now().isoformat().split(".")[0]
				types = {1:"Third Party Security Review", 2:"Full Audit"}
				createNewTest(x,y,types[random.randint(1,2)],"This is a test record created by a script","https://TestThirdParty" + str(x) + ".com","Some Limitations","TestContact " + str(y),timenow,str(random.randint(1,28)) + "/" + str(random.randint(1,12)) + "/2018","Some notes about a test created by a script")
				
	print("created lots of tests")
				
	for x in range(1,11):
		for y in range(1,21):
			for z in range(1,101): 
				if y % 2 == 0: 
					continue
				elif z % 2 == 0 or z % 3 == 0: 
					continue
				elif x < 6:
					ratings = {1: "Critical", 2: "High", 3: "Medium", 4: "Low"}
					titles = {1: "SQL Injection", 2: "Cross Site Scripting XSS", 3: "Deserialization Vulnerability", 4: "Cross Site Request Forgery CSRF", 5: "Sensitive Data Exposure"}
					statuses = {1: "Open", 2: "Closed", 3: "Risk Accepted"}
					createNewIssue(x,y,z,titles[random.randint(1,5)],"https://TestWebsite" + str(x) + "/vulnfunction.com","This is a test description for an issue created by the setup script","These are the sample remediation steps required to fix the issue created by the script",ratings[random.randint(1,4)],ratings[random.randint(1,4)],ratings[random.randint(1,4)],timenow,statuses[random.randint(1,3)], "These are the notes that accompany the issue created by the script")
				else: 
					ratings = {1: "Critical", 2: "High", 3: "Medium", 4: "Low"}
					titles = {1: "Lack of Encryption At Rest", 2: "Limited Employee Vetting", 3: "Limited Log Monitoring", 4: "Lack of Server Hardening", 5: "Segregation Of Duties"}
					statuses = {1: "Open", 2: "Closed", 3: "Risk Accepted"}
					createNewIssue(x,y,z,titles[random.randint(1,5)],"https://TestThirdParty" + str(x) + "/headquarters.com","This is a test description for an issue created by the setup script","These are the sample remediation steps required to fix the issue created by the script",ratings[random.randint(1,4)],ratings[random.randint(1,4)],ratings[random.randint(1,4)],timenow,statuses[random.randint(1,3)], "These are the notes that accompany the issue created by the script")
					
	print("created loads of issues")	

makeSomeData()
"""
