import psycopg2
import datetime
import random
import time

def createNewAsset(asset_name, asset_type, asset_owner, timestamp, asset_notes):

    sql = "INSERT INTO assets(asset_name,asset_type,asset_owner,created_on,asset_notes) VALUES (%s,%s,%s,%s,%s) RETURNING asset_id"
    try:
        conn = psycopg2.connect("dbname=reportatron host=127.0.0.1 user=webapp password=reportatron")
        cur = conn.cursor()
        cur.execute(sql, (asset_name, asset_type, asset_owner, timestamp, asset_notes,))
        assetId = cur.fetchall()[0][0]
        conn.commit()
        cur.close()
        return assetId
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.close()
        raise

def createNewEngagement(engform_location,main_contact,risk_rating,received_on,action_taken, eng_notes, eng_status):

    sqlCreateNewEngagement = "INSERT INTO engagements(engform_location,main_contact,risk_rating,received_on,action_taken, eng_notes,eng_status) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING eng_id"
    try:
        conn = psycopg2.connect("dbname=reportatron host=127.0.0.1 user=webapp password=reportatron")
        cur = conn.cursor()
        cur.execute(sqlCreateNewEngagement, (engform_location,main_contact,risk_rating,received_on,action_taken, eng_notes,eng_status,))
        engId = cur.fetchall()[0][0]
        conn.commit()
        cur.close()
        return engId
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.close()
        raise

def createAssetEngLink(link_asset_id, link_eng_id):

	sqlCreateAssetEngLink = "INSERT INTO links(link_asset_id, link_eng_id) VALUES (%s,%s)"
	try:
		conn = psycopg2.connect("dbname=reportatron host=127.0.0.1 user=webapp password=reportatron")
		cur = conn.cursor()
		cur.execute(sqlCreateAssetEngLink, (link_asset_id, link_eng_id,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def createAssetIssueLink(link_asset_id, link_issue_id):

	sqlCreateAssetIssueLink = "INSERT INTO issue_links(link_asset_id, link_issue_id) VALUES (%s,%s)"
	try:
		conn = psycopg2.connect("dbname=reportatron host=127.0.0.1 user=webapp password=reportatron")
		cur = conn.cursor()
		cur.execute(sqlCreateAssetIssueLink, (link_asset_id, link_issue_id,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		cur.close()
		raise

def createNewTest(eng_id,test_type,exec_summary,base_location,limitations,main_contact,created_on,test_date,test_notes):

    sqlCreateNewTest = "INSERT INTO tests(eng_id,test_type,exec_summary,base_location,limitations,main_contact,created_on,test_date,test_notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING test_id"
    try:
        conn = psycopg2.connect("dbname=reportatron host=127.0.0.1 user=webapp password=reportatron")
        cur = conn.cursor()
        cur.execute(sqlCreateNewTest, (eng_id,test_type,exec_summary,base_location,limitations,main_contact,created_on,test_date,test_notes,))
        testId = cur.fetchall()[0][0]
        conn.commit()
        cur.close()
        return testId
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.close()
        raise

def createNewIssue(eng_id,test_id,issue_title,issue_location,issue_description,remediation,risk_rating,risk_impact,risk_likelihood,created_on,issue_status,issue_details,issue_notes):

    sqlCreateNewIssue = "INSERT INTO issues(eng_id,test_id,issue_title,issue_location,issue_description,remediation,risk_rating,risk_impact,risk_likelihood,created_on,issue_status,issue_details,issue_notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING issue_id"
    try:
        conn = psycopg2.connect("dbname=reportatron host=127.0.0.1 user=webapp password=reportatron")
        cur = conn.cursor()
        cur.execute(sqlCreateNewIssue, (eng_id,test_id,issue_title,issue_location,issue_description,remediation,risk_rating,risk_impact,risk_likelihood,created_on,issue_status,issue_details,issue_notes,))
        issueId = cur.fetchall()[0][0]
        conn.commit()
        cur.close()
        return issueId
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.close()
        raise

    if risk_rating != 'Info':
        try:
        	conn = psycopg2.connect("dbname=reportatron host=127.0.0.1 user=webapp password=reportatron")
        	cur = conn.cursor()
        	cur.execute("UPDATE issues SET issue_due_date = CASE WHEN risk_rating LIKE 'Critical' THEN created_on + interval '7 days' WHEN risk_rating LIKE 'High' THEN created_on + interval '30 days' WHEN risk_rating LIKE 'Medium' THEN created_on + interval '60 days' WHEN risk_rating LIKE 'Low' THEN created_on + interval '180 days' END")
        	conn.commit()
        	cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
        	print(error)
        	cur.close()
        	raise


def makeSomeData():

    names = ["Adam Tron", "Babs Rapporta", "Cristina Postgressa", "David Flask", "Elvira Sequel", "Freddy Foryinz", "Bill Hicks", "Gerald Def"]
    ratings = {1: "Critical", 2: "High", 3: "Medium", 4: "Low"}
    titles = {1: "SQL Injection", 2: "Cross Site Scripting XSS", 3: "Deserialization Vulnerability", 4: "Cross Site Request Forgery CSRF", 5: "Sensitive Data Exposure"}
    titlesRA = {1: "Lack of Database Encryption", 2: "Change Control Not Enforced", 3: "No Segregation of Duties", 4: "Production Data in a Test Environment", 5: "Recovery Process Not Tested"}
    statuses = {1: "Open", 2: "Closed", 3: "Risk Accepted"}
    titlesTP = {1: "No Information Security Policy", 2: "Insufficient Employee Vetting", 3: "User Access Not Recertified Regularly", 4: "Inadequate Physical Security", 5: "No Vendor Risk Management Policy"}

    for i in range(1,6):
        timenow = datetime.datetime.now().isoformat().split(".")[0]
        index = random.randint(0,len(names)-1)
        assetOwner = names[index]
        newAsset = createNewAsset("TestWebsite " + str(i), "Application", assetOwner, timenow, "These are some notes about TestWebsite" + str(i))
        for y in range(1,3):
            index1 = random.randint(0,len(names)-1)
            engOwner = names[index1]
            newEng = createNewEngagement("F://TestWebsite" + str(i) + "//Project" + str(y), engOwner, ratings[random.randint(1,4)], str(random.randint(1,28)) + "/" + str(random.randint(1,12)) + "/2019", "Test email sent to main contact","Project to make some minor changes to the app", statuses[random.randint(1,2)])
            createAssetEngLink(newAsset, newEng)
            for z in range(1,2):
                index2 = random.randint(0,len(names)-1)
                testOwner = names[index2]
                newTest = createNewTest(newEng, "Application Security Test", "This is a summary for the Application Security Test for TestWebsite" + str(i) + ". Some testing was done and some results were produced.", "https://www.testwebsite" + str(i) + ".com", "None", testOwner, timenow, str(random.randint(1,28)) + "/" + str(random.randint(1,12)) + "/2019", "These are some notes for the testing of TestWebsite" + str(i))
                for j in range(1,10):
                    newIssue = createNewIssue(newEng, newTest, titles[random.randint(1,5)], "https://www.testwebsite" + str(i) + ".com", "This is the description of some issue found in an Application Security test", "This text would explain the best way to fix the issue found in the test", ratings[random.randint(1,4)], ratings[random.randint(1,4)], ratings[random.randint(1,4)], timenow, statuses[random.randint(1,3)], "A write up of the steps to reproduce the issue. These can include code, data dumps, step by step instructions etc.", "Some notes about the issue, when it will be fixed, what has been tried etc")
                    createAssetIssueLink(newAsset, newIssue)

                newTest2 = createNewTest(newEng, "Security Risk Assessment", "This is a summary for the Security Risk Assessment for TestWebsite" + str(i) + ". Some assessment was done and some results were produced.", "https://www.testwebsite" + str(i) + ".com", "None", testOwner, timenow, str(random.randint(1,28)) + "/" + str(random.randint(1,12)) + "/2019", "These are some notes for the assessment of TestWebsite" + str(i))
                for j in range(1,10):
                    newIssue = createNewIssue(newEng, newTest2, titlesRA[random.randint(1,5)], "https://www.testwebsite" + str(i) + ".com", "This is the description of some issue found in a Security Risk Assessment", "This text would explain the best way to fix the issue found in the Assessment", ratings[random.randint(1,4)], ratings[random.randint(1,4)], ratings[random.randint(1,4)], timenow, statuses[random.randint(1,3)], """A write up of the steps to reproduce the issue. /
                    These can include code, data dumps, step by step instructions etc.""", "Some notes about the issue, when it will be fixed, what has been tried etc")
                    createAssetIssueLink(newAsset, newIssue)

    for i in range(1,6):
        timenow = datetime.datetime.now().isoformat().split(".")[0]
        index = random.randint(0,len(names)-1)
        assetOwner = names[index]
        newAsset = createNewAsset("TestThirdParty " + str(i), "Third Party", assetOwner, timenow, "These are some notes about TestThirdParty" + str(i))
        for y in range(1,3):
            index1 = random.randint(0,len(names)-1)
            engOwner = names[index1]
            newEng = createNewEngagement("F://TestThirdParty" + str(i) + "//Project" + str(y), engOwner, ratings[random.randint(1,4)], str(random.randint(1,28)) + "/" + str(random.randint(1,12)) + "/2019", "Test email sent to main contact", "Project to send some data to a third party", statuses[random.randint(1,2)])
            createAssetEngLink(newAsset, newEng)
            for z in range(1,2):
                index2 = random.randint(0,len(names)-1)
                testOwner = names[index2]
                newTest = createNewTest(newEng, "Third Party Risk Assessment", "This is a summary for the Third Party Risk Assessment for TestThirdParty" + str(i) + ". Some assessing was done and some results were produced.", "A Third Party address, TestThirdParty" + str(i), "None", testOwner, timenow, str(random.randint(1,28)) + "/" + str(random.randint(1,12)) + "/2019", "These are some notes for the assessment TestThirdParty" + str(i))
                for j in range(1,10):
                    newIssue = createNewIssue(newEng, newTest, titlesTP[random.randint(1,5)], "TestThirdParty" + str(i) + " address", "This is the description of some issue found in a Third Party Risk Assessment", "This text would explain the best way to fix the issue found in the Assessment", ratings[random.randint(1,4)], ratings[random.randint(1,4)], ratings[random.randint(1,4)], timenow, statuses[random.randint(1,3)], """A write up of the steps to reproduce the issue. /
                    These can include code, data dumps, step by step instructions etc.""", "Some notes about the issue, when it will be fixed, what has been tried etc")
                    createAssetIssueLink(newAsset, newIssue)

    print("Created some assets")
    print("Created some engagements")
    print("Created some tests")
"""
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
"""

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
			else: import psycopg2
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
