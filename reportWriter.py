import markdown
import datetime

style = '<style>body { font-family: Verdana, Geneva, sans-serif; font-size: 16px; background-color: #f7fcff; line-height: 1.5; word-wrap: break-word; margin: 20px; padding: 45px; background-color: #fff; border: 1px solid #3EACBA; border-radius: 3px;} table { border-collapse: collapse; width: 100%; margin-bottom: 20px; border: 1px solid black;} th { background-color: #3EACBA; height: 50px; color: #fff;} th, td { text-align: center-left; border: 1px solid black; padding: 5px; text-align: left;} tr:nth-child(even) {background-color: #f2f2f2;} code { display: inline-block; overflow: visible; padding-left: 10px; padding-bottom: 10px; } pre { overflow: auto; font-size: 85%; background-color: #f6f8fa; border-radius: 3px; }</style>'
new_line = "\n"
double_new_line = "\n\n"

def get_date():
	return datetime.datetime.today().strftime('%d-%m-%y')
	
def writeTestReport(data, assetName, testData): 

	testType = testData[0][3]
	execSummary = testData[0][4]
	baseLocation = testData[0][5]
	limitations = testData[0][6]
	testDate = get_date()
	
	with open("./out/report.md", "w") as md_file: 
		
		md_file.write("#" + assetName + "_" + testType + "_" + testDate + double_new_line)
		md_file.write("#### Executive Summary" + double_new_line)
		md_file.write(execSummary + double_new_line)
		md_file.write("| **Description** | **Detail**|" + new_line)
		md_file.write("|---|---|" + new_line)
		md_file.write("| Asset | " + assetName + new_line)
		md_file.write("| Location | " + baseLocation + new_line)
		md_file.write("| Limitations | " + limitations + double_new_line)
		md_file.write("#### Technical Findings" + double_new_line)
	
		for issue in data: 
			issueTitle = issue[4]
			issueLocation = issue[5]
			issueDescription = issue[6]
			issueRemediation = issue[7]
			issueRisk = issue[8]
			issueImpact = issue[9]
			issueLikelihood = issue[10]
			issueStatus = issue[12]
			issueDetails = issue[14]
			issueID = issue[0]
		
			md_file.write("| **Ref** | " + str(issueID) + " - " + issueTitle + new_line)
			md_file.write("|---|---|" + new_line)
			md_file.write("| **Title** | " + issueTitle + new_line)
			md_file.write("| **Severity** | " + issueRisk + new_line)
			md_file.write("| **LIK** | " + issueLikelihood + new_line)
			md_file.write("| **IMP** | " + issueImpact + new_line)
			md_file.write("| **Description** | " + issueDescription + new_line)
			md_file.write("| **Resolution** | " + issueRemediation + double_new_line)
		
		md_file.write("#### Appendix" + double_new_line)
		
		for issue in data: 
			if issue[14] != None:
				
					md_file.write("```" + new_line)
					md_file.write(issueDetails + new_line)
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
		
	with open("./out/report.md", "r") as file: 
		infile = file.read()
	with open("./out/convert_md.html", "w") as outfile: 
		content = markdown.markdown(infile, extensions=['markdown.extensions.extra'])
		outfile.write(style)
		outfile.write(content)
		

def writeAssetReport(issueData, engCount, testData): 

	pass