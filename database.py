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

	def insertTableNames(self, tableName_1, tableName_2, tableName_3):
		self.visited = tableName_1
		self.scanResult = tableName_2
		self.urlQueue = tableName_3

	def closeDB(self):
		try:
			self.cursor.close()
			self.conn.close()
		except Exception as e:
			print("Database cannot close properly")

	def createVisitedTable(self, tableName):
		try:
			self.visited = tableName;
			self.cursor.execute("CREATE TABLE " + tableName + " ( url varchar(256) PRIMARY KEY , urlType numeric, domain varchar(128), isScanned boolean);")
			self.conn.commit()
		except Exception as e:
			print("Visited Table creation failed")		

	def createScanResultTable(self, tableName):
		try:
			self.scanResult = tableName;
			self.cursor.execute("CREATE TABLE " + tableName + " ( scanID varchar(64) PRIMARY KEY, url varchar(256) REFERENCES " + tableName_1 + "(url), result varchar(3000), status numeric );")
			self.conn.commit()
		except Exception as e:
			print("Scan Result Table creation failed")

	def createURLQueueTable(self, tableName):
		try:
			self.urlQueue = tableName
			self.cursor.execute("CREATE TABLE " + tableName + " ( id SERIAL, url varchar(256));")
			self.conn.commit()
		except Exception as e:
			print("URL Queue Table creation failed")				

	# Creates all the necessary tables
	def createCrawlerTables(self, tableName_1, tableName_2, tableName_3):
		try:
			self.visited = tableName_1
			self.scanResult = tableName_2
			self.urlQueue = tableName_3
			self.cursor.execute("CREATE TABLE " + tableName_1 + " ( url varchar(256) PRIMARY KEY , urlType numeric, domain varchar(128), isScanned boolean);")
			self.conn.commit()
			self.cursor.execute("CREATE TABLE " + tableName_2 + " ( scanID varchar(64) PRIMARY KEY, url varchar(256) REFERENCES " + tableName_1 + "(url), result varchar(3000), status numeric );")
			self.conn.commit()
			self.cursor.execute("CREATE TABLE " + tableName_3 + " ( id SERIAL, url varchar(256));")
			self.conn.commit()
		except Exception as e:
			print("Tables creation failed")

	def deleteVisitedTable(self):
		try: 
			self.cursor.execute("DROP TABLE " + self.scanResult + ";")
			self.conn.commit()
			self.cursor.execute("DROP TABLE " + self.urlQueue + ";")
			self.conn.commit()
			self.cursor.execute("DROP TABLE " + self.visited + ";")
			self.conn.commit()
		except Exception as e:
			print("Table cannot be dropped")
			self.conn.rollback()

	def deleteTable(self, tableName):
		try:
			self.cursor.execute("DROP TABLE " + tableName + ";")
			self.conn.commit()
		except Exception as e:
			print("Table " + tableName + " cannot be dropped")
			self.conn.rollback()

	# Deletes all the existing tables
	def deleteAllTablesWithNames(self, visitedTable, scanResultTable, urlQueueTable):
		try:
			""" DONT EVER RANDOMLY DROP TABLE. TABLE DROPPED CANNOT BE RECOVERED DONT PLAY PLAY """
			self.cursor.execute("DROP TABLE " + scanResultTable + ";")
			self.conn.commit()
			self.cursor.execute("DROP TABLE " + urlQueueTable + ";")
			self.conn.commit()
			self.cursor.execute("DROP TABLE " + visitedTable + ";")
			self.conn.commit()
		except Exception as e:
			print("Table cannot be dropped")
			self.conn.rollback()

	# Deletes all the existing tables
	def deleteAllTables(self):
		try:
			""" DONT EVER RANDOMLY DROP TABLE. TABLE DROPPED CANNOT BE RECOVERED DONT PLAY PLAY """
			self.cursor.execute("DROP TABLE " + self.scanResult + ";")
			self.conn.commit()
			self.cursor.execute("DROP TABLE " + self.urlQueue + ";")
			self.conn.commit()
			self.cursor.execute("DROP TABLE " + self.visited + ";")
			self.conn.commit()
		except Exception as e:
			print("Table cannot be dropped")
			self.conn.rollback()

	'''
	THIS PORTION IS FOR VISITED URL TABLE THAT IS USED BY THE CRAWLER
	'''
	def insertVisitedEntry(self, url, urlType, domain, isScanned):
		try:
			self.cursor.execute("INSERT INTO " + self.visited + " VALUES (%s, %s, %s, %s);", (url, str(urlType), domain, str(isScanned)))
			self.conn.commit()
		except Exception as e:
			print("Url: " + url + " cannot be inserted into table " + self.visited)
			self.conn.rollback()

	# Updates the isScanned column in the visited Table in accordance to the url provided
	# Input paramters (string, string, boolean) 
	def editVisitedScanEntry(self, url, isScanned):
		try:
			self.cursor.execute("UPDATE " + self.visited + " SET isScanned	= %s WHERE url = %s;", (str(isScanned), url))
			self.conn.commit()
		except Exception as e:
			print("Url: " + url + " cannot be updated")
			self.conn.rollback()

	def isVisited(self, url):
		try:		
			self.cursor.execute("SELECT url FROM " + self.visited + " WHERE url = '" + url + "';")
			rows = self.cursor.fetchall()
			if (len(rows) == 1):
				return True
			else:
				return False
		except Exception as e:
			print("Url: " + url + " cannot be selected from table " + self.visited)
			self.conn.rollback()

	def getVisitedEntriesByDomain(self, domain):
		try:		
			self.cursor.execute("SELECT url FROM " + self.visited + " WHERE domain = '" + domain + "';")
			rows = self.cursor.fetchall()
			if (len(rows) > 0):
				return True
			else:
				return False
		except Exception as e:
			print("Domain: " + domain + " cannot be selected from table " + self.visited)
			self.conn.rollback()

	'''
	THIS PORTION IS FOR SCAN RESULT TABLE THAT IS USED BY THE VIRUSTOTAL SENDER AND RECEIVER
	'''
	# Input parameters (string, string, string, string, int)
	def insertScanResultEntry(self, scanID, url, result, status):
		try:
			self.cursor.execute("INSERT INTO " + self.scanResult + " VALUES (%s, %s, %s, %s);", (scanID, url, result, str(status)))
			self.conn.commit()
		except Exception as e:
			print("Url: " + url + " cannot be inserted into table " + self.scanResult)
			self.conn.rollback()

	# Updates the status column (0, 1, -2 or 2) in the scan result table in accordance to scanID provided
	def editScanResultStatus(self, scanID, status):
		try:
			self.cursor.execute("UPDATE " + self.scanResult + " SET status = %s WHERE scanID = %s;", (str(status), scanID))
			self.conn.commit()
		except Exception as e:
			print("Status cannot be updated in URL: " + url + " of table " + self.scanResult)
			self.conn.rollback()	

	def updateScanResults(self, scanID, result):
		try:
			self.cursor.execute("UPDATE " + self.scanResult + " SET result = %s WHERE scanID = %s;", (result, scanID))
			self.conn.commit()
		except Exception as e:
			print("Result cannot be updated in URL: " + url + " of table " + self.scanResult)
			self.conn.rollback()	



	'''
	THIS PORTION IS FOR URL QUEUE TABLE THAT IS USED BY THE CRAWLER
	'''

	def push(self, url):
		try:
			self.cursor.execute("INSERT INTO " + self.urlQueue + " (url) VALUES ('" + url + "');")
			self.conn.commit()
		except Exception as e:
			print("Url: " + url + " cannot be inserted into table " + self.urlQueue)
			self.conn.rollback()

	def pop(self):
		try:
			self.cursor.execute("SELECT * FROM " + self.urlQueue + " ORDER BY id LIMIT 1;")
			row = self.cursor.fetchall()
			self.cursor.execute("DELETE FROM " + self.urlQueue + " WHERE id = '" + str(row[0][0]) + "';")
			self.conn.commit()
			return row[0][1]
		except Exception as e:
			print("Url: " + url + " cannot be popped from table " + self.urlQueue)
			self.conn.rollback()

	# Reset the serial sequence number
	# NOTE: restartValue MUST BE > 0
	def restartURLQueue(self, restartValue):
		try:
			self.cursor.execute("ALTER SEQUENCE " + self.urlQueue + "_id_seq RESTART WITH " + str(restartValue) + ";")
			self.conn.commit()
		except Exception as e:
			print("URL Queue Table serial ID cannot be restarted")
			self.conn.rollback()

	def exists(self, url):
		try:
			self.cursor.execute("SELECT * FROM " + self.urlQueue + " WHERE url = '" + url + "';")
			row = self.cursor.fetchall()		
			if (len(row) > 0):
				return True
			else:
				return False
		except Exception as e:
			print("Url: " + url + " cannot be popped from table " + self.urlQueue)
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
a.insertTableNames("visitedTable", "scanResultTable", "urlQueueTable")
# a.deleteTable("urlQueueTable")
# a.createURLQueueTable("urlQueueTable")
# a.createCrawlerTables("visitedTable", "scanResultTable", "urlQueueTable")
# a.insertVisitedEntry("visitedTable", "www.google.com.sg", 0, "www.google.com", False)
# a.editVisitedScanEntry("visitedTable", "www.google.com.sg", True)
# a.insertScanResultEntry("scanResultTable", "scanID_1", "www.google.com.sg", None, 0)
# a.editScanResultStatus("scanResultTable", "scanID_1", 2)
# a.insertURLQueueEntry("urlQueueTable", "www.google.com.sg")
# a.deleteURLQueueEntry("urlQueueTable", "www.google.com.sg")
# a.updateScanResults("scanResultTable", "scanID_1", None)
# a.restartURLQueue("urlQueueTable", 1)
# a.push("www.google.com.sg")
# a.push("www.google.com")

a.closeDB()

