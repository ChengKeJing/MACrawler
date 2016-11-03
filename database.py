import psycopg2
import sys

"""
INSTALL POSTGRES:
1. In terminal: sudo apt-get install postgresql libpq-dev postgresql-client postgresql-client-common
2. After installation: sudo -i -u postgres
3. In #postgres: createuser group11 -P --interactive
4. We set password as 12345 for now. Choose no, yes, yes
5. createdb MACdb
6. ctrl-d to exit postgres
7. In terminal: sudo apt-get install python-psycopg2
8. To import into crawler.py: from database import db



"""

class scanResults(object):
	fileName = ""
	scanID = ""
	permalink = ""

	def __init__(self):
		self.fileName = ""
		self.scanID = ""
		self.permalink = ""

	def setFileName(self, fileName):
		self.fileName = fileName

	def setScanID(self, scanID):
		self.scanID = scanID

	def setPermalink(self, permalink):
		self.permalink = permalink

	def getFileName(self):
		return self.fileName

	def getScanID(self):
		return self.scanID

	def getPermalink(self):
		return self.permalink

class db(object):
	# Initialization includes connection and creation of cursor
	def __init__(self):	
		try: 
			connect_str = "dbname='MACdb' user='group11' host='localhost' password='12345'"
			self.conn = psycopg2.connect(connect_str)
			self.cursor = self.conn.cursor()
		except Exception as e:
			print("Invalid dbname, user or password")

	def closeDB(self):
		try:
			self.cursor.close()
			self.conn.close()
		except Exception as e:
			print("Database cannot close properly")

	# Creates both visited table and fileData table
	def createCrawlerTables(self, tableName_1, tableName_2, tableName_3):
		try:
			self.cursor.execute("CREATE TABLE " + tableName_1 + " ( url varchar(256) PRIMARY KEY , urlType numeric, domain varchar(128), isScanned boolean);")
			self.conn.commit()
			self.cursor.execute("CREATE TABLE " + tableName_2 + " ( scanID varchar(64) PRIMARY KEY, url varchar(256) REFERENCES " + tableName_1 + "(url), result varchar(3000), status numeric );")
			self.conn.commit()
			self.cursor.execute("CREATE TABLE " + tableName_3 + " ( id SERIAL, url varchar(256));")
			self.conn.commit()
		except Exception as e:
			print("Visited Table creation failed")

	def deleteAllTables(self, tableName_1, tableName_2, tableName_3):
		try:
			""" DONT EVER RANDOMLY DROP TABLE. TABLE DROPPED CANNOT BE RECOVERED DONT PLAY PLAY """
			self.cursor.execute("DROP TABLE " + tableName_2 + ";")
			self.conn.commit()
			self.cursor.execute("DROP TABLE " + tableName_3 + ";")
			self.conn.commit()
			self.cursor.execute("DROP TABLE " + tableName_1 + ";")
			self.conn.commit()
		except Exception as e:
			print("Table cannot be dropped")
			self.conn.rollback()

	'''
	THIS PORTION IS FOR VISITED URL TABLE
	'''

	def insertVisitedEntry(self, tableName, url, urlType, domain, isScanned):
		try:
			self.cursor.execute("INSERT INTO " + tableName + " VALUES (%s, %s, %s, %s);", (url, str(urlType), domain, str(isScanned)))
			self.conn.commit()
		except Exception as e:
			print("Url: " + url + " cannot be inserted into table " + tableName)
			self.conn.rollback()

	def editVisitedScanEntry(self, tableName, url, isScanned):
		try:
			self.cursor.execute("UPDATE " + tableName + " SET isScanned	= %s WHERE url = %s;", (str(isScanned), url))
			self.conn.commit()
		except Exception as e:
			print("Url: " + url + " cannot be updated")
			self.conn.rollback()



	'''
	THIS PORTION IS FOR SCAN RESULT TABLE
	'''

	def insertScanResultEntry(self, tableName, scanID, url, result, status):
		try:
			self.cursor.execute("INSERT INTO " + tableName + " VALUES (%s, %s, %s, %s);", (scanID, url, result, str(status)))
			self.conn.commit()
		except Exception as e:
			print("Url: " + url + " cannot be inserted into table " + tableName)
			self.conn.rollback()

	def editScanResultStatus(self, tableName, scanID, status):
		try:
			self.cursor.execute("UPDATE " + tableName + " SET status = %s WHERE scanID = %s;", (str(status), scanID))
			self.conn.commit()
		except Exception as e:
			print("Url: " + url + " cannot be inserted into table " + tableName)
			self.conn.rollback()	



	'''
	THIS PORTION IS FOR URL QUEUE TABLE
	'''

	def insertURLQueueEntry(self, tableName, url):
		try:
			self.cursor.execute("INSERT INTO " + tableName + " (url) VALUES ('" + url + "');")
			self.conn.commit()
		except Exception as e:
			print("Url: " + url + " cannot be inserted into table " + tableName)
			self.conn.rollback()

	def deleteURLQueueEntry(self, tableName, url):
		try:
			self.cursor.execute("DELETE FROM " + tableName + " WHERE url = '" + url + "';")
			self.conn.commit()
		except Exception as e:
			print("Url: " + url + " cannot be deleted from table " + tableName)
			self.conn.rollback()

	def findVisitedEntry(self, url, tableName):
		try:
			self.cursor.execute("SELECT url from " + tableName + " WHERE url = " + "'" + url + "';")
			rows = self.cursor.fetchall()
			if (len(rows) == 1):
				return True
			else:
				return False
		except Exception as e:
			print("Error in fetch statement")
			self.conn.rollback()

	# Returns a list of scanResults objects
	def getAllScanResults(self):
		self.cursor.execute("SELECT * from scanResults")
		rows = self.cursor.fetchall()
		scanResultsList = []
		for i in rows:
			tempScanResults = scanResults()
			tempScanResults.setFileName(i[0])
			tempScanResults.setScanID(i[1])
			tempScanResults.setPermalink(i[2])
			scanResultsList.append(tempScanResults)
		return scanResultsList

	def getAllVisited(self):
		self.cursor.execute("SELECT * FROM visitedTable")
		rows = self.cursor.fetchall()
		output = open('output.txt', 'w+')
		for i in rows:
			output.write("URL: " + i[0] + "\n")
			output.write("File Data: " + str(i[1]) + "\n\n")
		output.close()


a = db()
# a.deleteAllTables("visitedTable", "scanResultTable", "urlQueueTable")
# a.createCrawlerTables("visitedTable", "scanResultTable", "urlQueueTable")
# a.insertVisitedEntry("visitedTable", "www.google.com.sg", 0, "www.google.com", False)
# a.editVisitedScanEntry("visitedTable", "www.google.com.sg", True)
# a.insertScanResultEntry("scanResultTable", "scanID_1", "www.google.com.sg", None, 0)
# a.editScanResultStatus("scanResultTable", "scanID_1", 2)
# a.insertURLQueueEntry("urlQueueTable", "www.google.com.sg")
# a.deleteURLQueueEntry("urlQueueTable", "www.google.com.sg")


a.closeDB()

