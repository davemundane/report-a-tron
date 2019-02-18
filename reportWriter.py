import markdown
import datetime

style = '<style>body { font-family: Verdana, Geneva, sans-serif; font-size: 16px; background-color: #f7fcff; line-height: 1.5; word-wrap: break-word; margin: 20px; padding: 45px; background-color: #fff; border: 1px solid #6a1a41; border-radius: 3px;} table { border-collapse: collapse; width: 100%; margin-bottom: 20px; border: 1px solid black;} th { background-color: #6a1a41; height: 50px; color: #fff;} th, td { text-align: center-left; border: 1px solid black; padding: 5px; text-align: left;} tr:nth-child(even) {background-color: #f2f2f2;} code { display: inline-block; overflow: visible; padding-left: 10px; padding-bottom: 10px; } pre { overflow: auto; font-size: 85%; background-color: #f6f8fa; border-radius: 3px; }</style>'
new_line = "\n"
double_new_line = "\n\n"

def get_date():
	return datetime.datetime.today().strftime('%d-%m-%y')
	
def writeTestReport(data, assetName, testData): 

	testType = testData[0][2]
	execSummary = testData[0][3]
	baseLocation = testData[0][4]
	limitations = testData[0][5]
	testDate = get_date()
	
	with open("./templates/report.md", "w") as md_file: 
	
		if assetName: 
			md_file.write("#" + assetName + "_" + testType + "_" + testDate + double_new_line)
		md_file.write("#### Executive Summary" + double_new_line)
		md_file.write(execSummary + double_new_line)
		
		if assetName: 
			md_file.write("| **Description** | **Detail**|" + new_line)
			md_file.write("|---|---|" + new_line)
			md_file.write("| Asset | " + assetName + new_line)
			md_file.write("| Location | " + baseLocation + new_line)
			md_file.write("| Limitations | " + limitations + double_new_line)
		
		md_file.write("#### Issue Summary" + double_new_line)
			
		md_file.write("|**Issue Ref** | **Issue Title** | **Rating** | **Status** | " + new_line)
		md_file.write("|--|--|--|--|" + new_line)
		
		for issue in data: 
			issueTitle = issue[3]
			issueLocation = issue[4]
			issueDescription = issue[5]
			issueRemediation = issue[6]
			issueRisk = issue[7]
			issueImpact = issue[8]
			issueLikelihood = issue[9]
			issueStatus = issue[12]
			issueDetails = issue[14]
			issueID = issue[0]
		
			md_file.write("| " + str(issueID) + " | " + issueTitle + " | " + issueRisk + " | " + issueStatus + " | " + new_line)

		md_file.write(double_new_line)
		md_file.write("#### Technical Findings" + double_new_line)
	
		for issue in data: 
			issueTitle = issue[3]
			issueLocation = issue[4]
			issueDescription = issue[5]
			issueRemediation = issue[6]
			issueRisk = issue[7]
			issueImpact = issue[8]
			issueLikelihood = issue[9]
			issueStatus = issue[12]
			issueDetails = issue[13]
			issueID = issue[0]
				
			md_file.write("| **Ref** | " + str(issueID) + " - " + issueTitle + new_line)
			md_file.write("|---|---|" + new_line)
			md_file.write("| Status | " + issueStatus + new_line)
			md_file.write("| Issue Title | " + issueTitle + new_line)
			md_file.write("| Risk Rating | " + issueRisk + new_line)
			md_file.write("| Description | " + issueDescription + new_line)
			md_file.write("| Remediation | " + issueRemediation + double_new_line)
		
		md_file.write("#### Appendix" + double_new_line)
		
		for issue in data: 
			if issue[13]:
				md_file.write(str(issue[0]) + " - " + issue[3] + new_line) 
				md_file.write("```" + new_line)
				md_file.write(issue[13] + new_line)
				md_file.write("```" + double_new_line)
			else:
				continue
				
		md_file.write("**Remediation Timelines**" + double_new_line)
		md_file.write("|Issue Rating|Remediation Time|" + new_line)
		md_file.write("|----:|----|" + new_line)
		md_file.write("|Critical| 7 Days|" + new_line)
		md_file.write("|High| 30 Days|" + new_line)
		md_file.write("|Medium| 60 Days|" + new_line)
		md_file.write("|Low|180 Days|" + double_new_line)
		
	with open("./templates/report.md", "r") as file: 
		infile = file.read()
	with open("./templates/convert_md.html", "w") as outfile: 
		content = markdown.markdown(infile, extensions=['markdown.extensions.extra'])
		outfile.write(style)
		outfile.write(content)
		

def writeAssetReport(issueData, engCount, testData): 

	pass
