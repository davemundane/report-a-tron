from flask import Flask, render_template, request, redirect, url_for
import random
import json
import datetime
import requests
import markdown
import configparser
import dbstuff
import reportWriter
import theStatMachine as stat


# root handler to serve the index page
app = Flask(__name__)
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

@app.route("/gethtmlreport")
def gethtmlreport(): 
	return render_template('convert_md.html')
	
@app.route("/thedata")
def thedata():
	data = dbstuff.getAllAssetTableData()
	return render_template('thedata.html', data=data)
	
@app.route("/appdata", methods=['GET'])
def appdata():
	app_id = request.args.get('appID')
	data = dbstuff.getSingleAssetTestData(asset_id)
	return render_template('appdata.html', data=data)

@app.route("/report")
def report():
	return render_template('report.html')

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

@app.route("/orphanengagement", methods=['GET'])
def orphanengagement():
        return render_template("orphanengagement.html")
	
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

@app.route("/neworphanengagement", methods=['POST'])
def neworphanengagement():
        _engformLocation = request.form['engformLocation']
        _mainContact = request.form['mainContact']
        _riskRating = request.form['riskRating']
        _receivedOn = request.form['receivedOn']
        _actionTaken = request.form['actionTaken']
        _engNotes = request.form['engNotes']
        try: 
                timenow = datetime.datetime.now().isoformat().split(".")[0]
                dbstuff.createNewEngagement(None,_engformLocation,_mainContact,_riskRating,_receivedOn,_actionTaken,_engNotes)
                return redirect(url_for("thedata"))
        except: 
                return redirect(url_for("error"))
				
@app.route("/openengagements")
def openengagements(): 
	data = dbstuff.getOpenEngagementData()
	return render_template('viewengagements.html', data=data)
	
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
		
@app.route("/updateEng")
def updateEng():
	_engID = request.args.get('engID')
	data = dbstuff.getSingleEngagement(_engID)
	return render_template('updateeng.html', data=data)
	
@app.route("/updateengagement", methods=['POST'])
def updateengagement(): 
	_engID = request.form['engId']
	_engformLocation = request.form['engformLocation']
	_mainContact = request.form['mainContact']
	_riskRating = request.form['riskRating']
	_receivedOn = request.form['receivedOn']
	_actionTaken = request.form['actionTaken']
	_engNotes = request.form['engNotes']
	_engStatus = request.form['engStatus']
	try: 
		dbstuff.updateEngagement(_engID,_engformLocation,_mainContact,_riskRating,_receivedOn,_actionTaken,_engNotes,_engStatus)
		return redirect(url_for("viewengagements"))
	except: 
		return redirect(url_for("error"))
		
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
		print(_assetID,_engID,_testType,_execSummary,_baseLocation,_limitations,_mainContact,timenow,_testDate,_testNotes)
		dbstuff.createNewTest(_engID,_testType,_execSummary,_baseLocation,_limitations,_mainContact,timenow,_testDate,_testNotes)
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
	_issueStatus = request.form['issueStatus']
	_issueTitle = request.form['issueTitle']
	_riskRating = request.form['riskRating']
	_riskImpact = request.form['riskImpact']
	_riskLikelihood = request.form['riskLikelihood']
	_location = request.form['location']
	_description = request.form['description']
	_remediation = request.form['remediation']
	_issueDetails = request.form['issueDetails']
	_issueNotes = request.form['issueNotes']
	_issueRADate = request.form['issueRADate']
	_issueRAOwner = request.form['issueRAOwner']
	_issueRAExpiry = request.form['issueRAExpiry']
	_issueRANotes = request.form['issueRANotes']
	try: 
		dbstuff.updateSingleIssue(_issueTitle,_riskRating,_riskImpact,_riskLikelihood,_location,_issueStatus,_description,_remediation,_issueDetails,_issueNotes,_issueRADate,_issueRAOwner,_issueRAExpiry,_issueRANotes,_issueID)
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
		dbstuff.createNewIssue(_engID,_testID,_issueTitle,_issueLocation,_issueDescription,_remediation,_riskRating,_riskImpact,_riskLikelihood,timenow,_status,_issueDetails,_issueNotes)
	except Exception as error:
		print(error)
		return redirect(url_for("error"))
	return redirect(url_for("createnewissue", assetID=_assetID, engID=_engID, testID=_testID))


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
	return gethtmlreport()

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
			return gethtmlreport()
		except: 
			return render_template('error.html')
			
@app.route("/stats")
def stats():
	return render_template('stats.html')
	
@app.route("/viewstats", methods=['POST'])
def viewstats():

	_startDate = request.form['startDate']
	_endDate = request.form['endDate']
	
	getStats = stat.ReportatronStats()
	data = getStats.getAllTheStats(_startDate, _endDate)
	
	return render_template('viewstats.html', data=data)
			
@app.route("/search")
def search(): 
	_searchTerm = request.args.get('searchTerm')
	data = dbstuff.getAssetIdFromSearch(_searchTerm)
	return render_template('thedata.html', data=data)
	
if __name__ == "__main__":
	#config = configparser.ConfigParser()
	#config.read('default.conf')
	#hostIP = config['DEFAULT']['host']
	app.run()

