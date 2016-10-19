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


	def getAllEntries(self):
		self.cursor.execute("SELECT * from test")
		rows = self.cursor.fetchall()
		print(rows)

a = db()
a.deleteTable("visitedURLs")
a.createVisitedTable("visitedURLs")
a.insertVisitedEntry("www.google.com", "visitedURLs")
a.insertVisitedEntry("www.google.com", "visitedURLs")
success = a.findVisitedEntry("www.google.com", "visitedURLs")
fail = a.findVisitedEntry("www.goomei.com", "visitedURLs")
print("Searching www.google.com: " + str(success))
print("Searching www.goomei.com: " + str(fail))
a.closeDB()
