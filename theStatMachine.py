import psycopg2
import requests
import datetime

class ReportatronStats: 

	def __init__(self): 
		
		self.conn = psycopg2.connect("dbname=reportatron host=127.0.0.1 user=webapp password=reportatron")
		
	def getAllTheStats(self, start_date, end_date): 
	
		try: 
			cur = self.conn.cursor()
			sqlEngagements = "SELECT COUNT(engagements.eng_id) FROM engagements WHERE engagements.received_on >= %s AND engagements.received_on <= %s"
			cur.execute(sqlEngagements, (start_date, end_date,))
			engMonth = cur.fetchall()[0][0]
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			cur.close()
			pass
			
		try: 
			cur = self.conn.cursor()
			sqlOpenEngagements = "SELECT COUNT(engagements.eng_id) FROM engagements WHERE engagements.eng_status LIKE 'Open'"
			cur.execute(sqlOpenEngagements)
			openEng = cur.fetchall()[0][0]
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			cur.close()
			pass
			
		try: 
			cur = self.conn.cursor()
			sqlOpenIssues = "SELECT COUNT (issues.issue_id) FROM issues LEFT JOIN issue_links ON issues.issue_id=issue_links.link_issue_id LEFT JOIN assets ON assets.asset_id=issue_links.link_asset_id WHERE issues.issue_status LIKE 'Open'"
			cur.execute(sqlOpenIssues)
			openIssues = cur.fetchall()[0][0]
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			cur.close()
			pass
			
		try: 
			cur = self.conn.cursor()
			sqlOpenIssues = "SELECT COUNT (issues.issue_id) FROM issues LEFT JOIN issue_links ON issues.issue_id=issue_links.link_issue_id LEFT JOIN assets ON assets.asset_id=issue_links.link_asset_id WHERE issues.issue_status LIKE 'Open' AND issues.risk_rating LIKE 'Critical'"
			cur.execute(sqlOpenIssues)
			critIssues = cur.fetchall()[0][0]
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			cur.close()
			pass
		
		try: 
			cur = self.conn.cursor()
			sqlOpenIssues = "SELECT COUNT (issues.issue_id) FROM issues LEFT JOIN issue_links ON issues.issue_id=issue_links.link_issue_id LEFT JOIN assets ON assets.asset_id=issue_links.link_asset_id WHERE issues.issue_status LIKE 'Open' AND issues.risk_rating LIKE 'High'"
			cur.execute(sqlOpenIssues)
			highIssues = cur.fetchall()[0][0]
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			cur.close()
			pass
			
		try: 
			cur = self.conn.cursor()
			sqlOpenIssues = "SELECT COUNT (issues.issue_id) FROM issues LEFT JOIN issue_links ON issues.issue_id=issue_links.link_issue_id LEFT JOIN assets ON assets.asset_id=issue_links.link_asset_id WHERE issues.issue_status LIKE 'Open' AND issues.risk_rating LIKE 'Medium'"
			cur.execute(sqlOpenIssues)
			medIssues = cur.fetchall()[0][0]
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			cur.close()
			pass
			
		try: 
			cur = self.conn.cursor()
			sqlOpenIssues = "SELECT COUNT (issues.issue_id) FROM issues LEFT JOIN issue_links ON issues.issue_id=issue_links.link_issue_id LEFT JOIN assets ON assets.asset_id=issue_links.link_asset_id WHERE issues.issue_status LIKE 'Open' AND issues.risk_rating LIKE 'Low'"
			cur.execute(sqlOpenIssues)
			lowIssues = cur.fetchall()[0][0]
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			cur.close()
			pass

		try: 
			cur = self.conn.cursor()
			sqlInternetFacingApps = "SELECT COUNT(assets.asset_id) FROM assets WHERE assets.asset_name LIKE '%Internet Facing App%'"
			cur.execute(sqlInternetFacingApps)
			intApps = cur.fetchall()[0][0]
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			cur.close()
			pass

		try: 
			cur = self.conn.cursor()
			sqlInternetFacingAppsIssues = "SELECT COUNT (issues.issue_id) FROM issues LEFT JOIN issue_links ON issues.issue_id=issue_links.link_issue_id LEFT JOIN assets ON assets.asset_id=issue_links.link_asset_id WHERE assets.asset_name LIKE '%Internet Facing%' AND issues.issue_status LIKE 'Open'"
			cur.execute(sqlInternetFacingAppsIssues)
			intAppIssues = cur.fetchall()[0][0]
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			cur.close()
			pass
			
		try: 
			cur = self.conn.cursor()
			sqlThirdPartyEngagements = "SELECT COUNT(DISTINCT engagements.eng_id) FROM engagements LEFT JOIN links ON links.link_eng_id=engagements.eng_id LEFT JOIN assets ON assets.asset_id=links.link_asset_id WHERE engagements.received_on >= %s AND engagements.received_on <= %s AND assets.asset_type LIKE 'Third Party'"
			cur.execute(sqlThirdPartyEngagements, (start_date, end_date,))
			tpEngs = cur.fetchall()[0][0]
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			cur.close()
			pass

		try: 
			cur = self.conn.cursor()
			sqlThirdPartyIssues = "SELECT COUNT (issues.issue_id) FROM issues LEFT JOIN issue_links ON issues.issue_id=issue_links.link_issue_id LEFT JOIN assets ON assets.asset_id=issue_links.link_asset_id WHERE assets.asset_type LIKE '%Third%' AND issues.issue_status LIKE 'Open'"
			cur.execute(sqlThirdPartyIssues)
			tpIssues = cur.fetchall()[0][0]
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
			cur.close()
			pass


		othEng = engMonth - tpEngs
		othEngIssues = openIssues - tpIssues

		return ({"EngagementsMonth": engMonth, "OpenEngagements": openEng, "TotalIssues": openIssues, "issues": {"Critical": critIssues, "High": highIssues, "Medium": medIssues, "Low": lowIssues}, "InternetApps": intApps, "InternetIssues": intAppIssues, "ThirdPartyEngagements": tpEngs, "ThirdPartyIssues": tpIssues, "OtherEngagements": othEng, "OtherEngagementIssues": othEngIssues})

