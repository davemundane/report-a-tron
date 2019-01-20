from flask import Flask, render_template, request, redirect, url_for
import random
import json
import datetime
import requests
import markdown
import configparser
import dbstuff
import reportWriter

finding_dict = {}
ticker = 0
UPLOAD_FOLDER = "."
_asvName = ""
style = '<style>body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; font-size: 16px; line-height: 1.5; word-wrap: break-word; padding: 45px; word-wrap: break-word; background-color: #fff; border: 1px solid #ddd; border-bottom-right-radius: 3px; border-bottom-left-radius: 3px;} table { border-collapse: collapse; } th {    background-color: #003A6F;    color: white;}table, th, td {    border: 1px solid black;}table {    width: 90%; margin-bottom: 20px; margin-left: 5%; margin-right: 5%; } th {    height: 50px;}th, td {    text-align: center-left;}th, td {    padding: 5px;    text-align: left;}tr:nth-child(even) {background-color: #f2f2f2;}code {  display: inline-block;  line-height: 20px  margin: 10px;  padding: 10px;  } code { display: inline; max-width: auto; padding: 0; margin: 0; overflow: visible; line-height: inherit; word-wrap: normal; background-color: transparent; border: 0;} pre { padding: 16px; overflow: auto; font-size: 85%; line-height: 1.45; background-color: #f6f8fa; border-radius: 3px; word-wrap: normal }</style>'

# root handler to serve the index page
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route("/")
def main():
	return render_template('index.html')
	
@app.route("/newapp")
def newapp():
	return render_template('newapp.html')
	
@app.route("/error")
def error():
	return render_template('error.html')
	
@app.route("/complete")
def complete():
	return render_template('complete.html')
	
@app.route("/thedata")
def thedata():
	data = dbstuff.getAllAssetTableData()
	return render_template('thedata.html', data=data)
	
@app.route("/appdata", methods=['GET'])
def appdata():
	app_id = request.args.get('appID')
	data = dbstuff.getSingleAssetTestData(asset_id)
	return render_template('appdata.html', data=data)

# handler to show the report page containing the main form
@app.route("/report")
def report():
	return render_template('report.html')

# handler for an endpoint to receive the data from index, asvname etc
@app.route("/createapp", methods=['POST'])
def createapp():
	_assetName = request.form['assetName']
	_assetType = request.form['assetType']
	_assetOwner = request.form['assetOwner']
	_assetNotes = request.form['assetNotes']
	try: 
		timenow = datetime.datetime.now().isoformat().split(".")[0]
		dbstuff.createNewAsset(_assetName, _assetType, _assetOwner, timenow, _assetNotes)
		return redirect(url_for("thedata"))
	except: 
		return redirect(url_for("error"))
	
@app.route("/engagements", methods=['GET'])
def engagements():
	assetName = request.args.get('assetName')
	assetID = request.args.get('assetID')
	return render_template("engagements.html", assetName=assetName, assetID=assetID)
	
# handler for an endpoint to receive the data from newengagements etc
@app.route("/newengagement", methods=['POST'])
def newengagement():
	_assetID = request.form['assetID']
	_engformLocation = request.form['engformLocation']
	_mainContact = request.form['mainContact']
	_riskRating = request.form['riskRating']
	_receivedOn = request.form['receivedOn']
	_actionTaken = request.form['actionTaken']
	_engNotes = request.form['engNotes']
	try: 
		timenow = datetime.datetime.now().isoformat().split(".")[0]
		dbstuff.createNewEngagement(_assetID,_engformLocation,_mainContact,_riskRating,_receivedOn,_actionTaken,_engNotes)
		return redirect(url_for("thedata"))
	except: 
		return redirect(url_for("error"))
	
@app.route("/viewengagements")
def viewengagements():
	assetID = request.args.get('assetID')
	assetName = request.args.get('assetName')
	if assetID:
		data = dbstuff.getEngagementsForAsset(assetID)
		return render_template('viewengagements.html', data=data, assetName=assetName)
	else: 
		data = dbstuff.getAllEngagementData()
		return render_template('viewengagements.html', data=data)
	
@app.route("/newtest", methods=['GET'])
def newtest():
	assetID = request.args.get('assetID')
	engID = request.args.get('engID')
	return render_template('newtest.html', assetID=assetID, engID=engID)
	
@app.route("/createtest", methods=['POST'])
def createtest():
	_assetID = request.form['assetID']
	_engID = request.form['engID']
	_testType = request.form['testType']
	_execSummary = request.form['execSummary']
	_baseLocation = request.form['baseLocation']
	_limitations = request.form['limitations']
	_mainContact = request.form['mainContact']
	_testDate = request.form['testDate']
	_testNotes = request.form['testNotes']
	try: 
		timenow = datetime.datetime.now().isoformat().split(".")[0]
		dbstuff.createNewTest(_assetID,_engID,_testType,_execSummary,_baseLocation,_limitations,_mainContact,timenow,_testDate,_testNotes)
		return redirect(url_for("thedata"))
	except: 
		return redirect(url_for("error"))
	
	
@app.route("/viewtests", methods=['GET'])
def viewtests():
	engID = request.args.get('engID')
	assetID = request.args.get('assetID')
	assetName = request.args.get('assetName')
	if engID:
		data = dbstuff.getTestsForEngagement(engID)
		return render_template('viewtests.html', data=data, assetName=assetName)
	if assetID:
		data = dbstuff.getTestsForAsset(assetID)
		return render_template('viewtests.html', data=data, assetName=assetName)
	else: 
		data = dbstuff.getAllTestData()
		return render_template('viewtests.html', data=data)
		
		
@app.route("/viewissues", methods=['GET'])
def viewissues():
	engID = request.args.get('engID')
	assetID = request.args.get('assetID')
	testID = request.args.get('testID')
	assetName = request.args.get('assetName')
	if testID:
		data = dbstuff.getIssuesForTest(testID)
		return render_template('viewissues.html', data=data, assetName=assetName)
	if assetID:
		data = dbstuff.getIssuesForAsset(assetID)
		return render_template('viewissues.html', data=data, assetName=assetName)
	else: 
		data = dbstuff.getAllIssueData()
		return render_template('viewissues.html', data=data)
		
@app.route("/updateissue", methods=['GET'])
def updateissue():
	issueID = request.args.get('issueID')
	try: 
		data = dbstuff.getSingleIssue(issueID)
		return render_template("updateissue.html", data=data, issueID=issueID)
	except: 
		return render_template("updateissue.html", issueID=issueID)
		
@app.route("/updatesingleissue", methods=['POST'])
def updatesingleissue():
	_issueID = request.form['issueID']
	_status = request.form['status']
	try: 
		dbstuff.updateSingleIssue(_status,_issueID)
		return redirect(url_for("viewissues"))
	except: 
		return redirect(url_for("error"))
		
@app.route("/createissue", methods=['POST'])
def createissue():
	_assetID = request.form['assetID']
	_engID = request.form['engID']
	_testID = request.form['testID']
	_issueTitle = request.form['issueTitle']
	_issueLocation = request.form['issueLocation']
	_issueDescription = request.form['issueDescription']
	_remediation = request.form['remediation']
	_riskRating = request.form['riskRating']
	_riskImpact = request.form['riskImpact']
	_riskLikelihood = request.form['riskLikelihood']
	_status = request.form['status']
	_issueDetails = request.form['appendix']
	_issueNotes = request.form['issueNotes']
	try: 
		timenow = datetime.datetime.now().isoformat().split(".")[0]
		dbstuff.createNewIssue(_assetID,_engID,_testID,_issueTitle,_issueLocation,_issueDescription,_remediation,_riskRating,_riskImpact,_riskLikelihood,timenow,_status,_issueDetails,_issueNotes)
	except: 
		return redirect(url_for("error"))
	return redirect(url_for("createnewissue"))
	
@app.route("/createnewissue", methods=['GET'])
def createnewissue():
	_assetID = request.args.get('assetID')
	_engID = request.args.get('engID')
	_testID = request.args.get('testID')
	return render_template("createnewissue.html", assetID=_assetID, engID=_engID, testID=_testID)

@app.route("/testreport", methods=['GET'])
def testreport():
	_testID = request.args.get('testID')
	_assetName = request.args.get('assetName')
	testData = dbstuff.getTestDataForReport(_testID)
	issueData = dbstuff.getIssuesForTest(_testID)
	reportWriter.writeTestReport(issueData, _assetName, testData)
	return render_template('testreport.html')

@app.route("/adhocreport", methods=['GET'])
def adhocreport():
	return render_template('adhocreport.html')
	
@app.route("/writeadhocreport", methods=['POST'])
def writeadhocreport():
	_assetName = request.form['assetName']
	_issuesOpen = request.form.get('issuesOpen')
	if _issuesOpen: 
		_issuesOpen = "Open"
	_issuesClosed = request.form.get('issuesClosed')
	if _issuesClosed: 
		_issuesClosed = "Closed"
	_issuesRA = request.form.get('issuesRA')
	if _issuesRA: 
		_issuesRA = "Risk Accepted"
	print(_issuesOpen, _issuesClosed, _issuesRA)
	_reportType = request.form['reportType']
	
	assetID = dbstuff.getAssetIdFromTitle(_assetName)[0]
	if _reportType == "testReport":
		pass
	elif _reportType == "engagementReport":
		pass
	elif _reportType == "assetReport": 
		try: 
			issueData = dbstuff.getIssuesForAsset(assetID)
			print(issueData)
			engCount = dbstuff.countEngagementsForAsset(assetID)
			print(engCount)
			testData = dbstuff.getTestsForAsset(assetID)
			print(testData)
			reportWriter.writeAssetReport(issueData, engCount, testData)
			return render_template('complete.html')
		except: 
			return render_template('error.html')
	
if __name__ == "__main__":
	#config = configparser.ConfigParser()
	#config.read('default.conf')
	#hostIP = config['DEFAULT']['host']
	app.run()