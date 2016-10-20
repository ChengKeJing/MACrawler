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

	def createVisitedTable(self, tableName):
		try:
			self.cursor.execute("CREATE TABLE " + tableName + " ( url varchar(256) PRIMARY KEY );")
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


	def insertVisitedEntry(self, url, tableName):
		try:
			self.cursor.execute("INSERT INTO " + tableName + " VALUES (" + "'" + url + "');")
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
			self.cursor.execute("SELECT * from " + tableName + " WHERE url = " + "'" + url + "';")
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


"""a = db()
resultList = a.getAllScanResults()
for i in resultList:
	print(i.getFileName() + " | " + i.getScanID() + " | " + i.getPermalink() + "\n")
a.closeDB()
"""
