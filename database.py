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
	def createCrawlerTables(self, tableName_1, tableName_2):
		try:
			self.cursor.execute("CREATE TABLE " + tableName_1 + " ( url varchar(256) PRIMARY KEY , fileData bytea );")
			self.conn.commit()
			self.cursor.execute("CREATE TABLE " + tableName_2 + " ( fileData bytea PRIMARY KEY , isSafe boolean );")
			self.conn.commit()
		except Exception as e:
			print("Visited Table creation failed")

	def createScanResultTable(self, tableName):
		try:
			self.cursor.execute("CREATE TABLE " + tableName + " ( fileName varchar(256) PRIMARY KEY , scanID varchar(100) , permalink varchar(256) );")
			self.conn.commit()
		except Exception as e:
			print("Scan Result Table creation failed")

	def deleteTable(self, tableName):
		try:
			""" DONT EVER RANDOMLY DROP TABLE. TABLE DROPPED CANNOT BE RECOVERED DONT PLAY PLAY """
			self.cursor.execute("DROP TABLE " + tableName + ";")
			self.conn.commit()
		except Exception as e:
			print("Table cannot be dropped")
			self.conn.rollback()


	def insertVisitedEntry(self, tableName, url, fileData):
		try:
			if fileData is None:
				self.cursor.execute("INSERT INTO " + tableName + " VALUES (%s, %s);", (url, fileData))
			else:
				self.cursor.execute("INSERT INTO " + tableName + " VALUES (%s, %s);", (url, psycopg2.Binary(fileData)))
			self.conn.commit()
		except Exception as e:
			print("Url: " + url + " cannot be inserted into table " + tableName)
			self.conn.rollback()

	def insertScanResult(self, tableName, fileID, scanID, permalink):
		try:
			self.cursor.execute("INSERT INTO " + tableName + " VALUES (" + "'" + fileID + "', '" + scanID + "', '" + permalink + "');")
			self.conn.commit()
		except Exception as e:
			print("Url: " + url + " cannot be inserted into table " + tableName)
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
a.deleteTable("visitedTable")
a.deleteTable("fileDataTable")
a.createCrawlerTables("visitedTable", "fileDataTable")
inputFile = open('file1', 'r')
fileData = inputFile.read()
"""print(psycopg2.Binary(fileData))"""
a.insertVisitedEntry("visitedTable", "www.yahoo.com", fileData)
a.insertVisitedEntry("visitedTable", "www.google.com", None)
inputFile.close()
a.getAllVisited()
a.closeDB()

