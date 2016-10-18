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
	def __init__(self):	
		try: 
			connect_str = "dbname='MACdb' user='group11' host='localhost' password='12345'"
			self.conn = psycopg2.connect(connect_str)
			self.cursor = self.conn.cursor()
		except Exception as e:
			print("Invalid dbname, user or password")
			print(e)

	def getAllEntries(self):
		self.cursor.execute("SELECT * from test")
		rows = self.cursor.fetchall()
		print(rows)

	def createVisitedTable(self, tableName):
		try:
			self.cursor.execute("CREATE TABLE " + tableName + " ( url varchar(256) PRIMARY KEY );")
			self.conn.commit()
		except Exception as e:
			print("Table creation failed")

	def deleteTable(self, tableName):
		try:
			""" DONT EVER RANDOMLY DROP TABLE. TABLE DROPPED CANNOT BE RECOVERED DONT PLAY PLAY """
			self.cursor.execute("DROP TABLE " + tableName + ";")
			self.conn.commit()
		except Exception as e:
			print("Table cannot be dropped")

	def insertVisitedEntry(self, url, tableName):
		try:
			self.cursor.execute("INSERT INTO " + tableName + " VALUES (" + "'" + url + "');")
			self.conn.commit()
		except Exception as e:
			print("Url: " + url + " cannot be inserted into table " + tableName)
			self.conn.rollback()

	def findVisitedEntry(self, url, tableName):
		try:
			self.cursor.execute("SELECT * from " + tableName + " WHERE url = " + "'" + url + "';")
			rows = self.cursor.fetchall()
			print(rows)
		except Exception as e:
			print("Error in fetch statement")
			self.conn.rollback()

"""
a = db()
a.createVisitedTable("visitedURLs")
a.insertVisitedEntry("www.google.com", "visitedURLs")
a.insertVisitedEntry("www.google.com", "visitedURLs")
a.findVisitedEntry("www.google.com", "visitedURLs")
a.cursor.close()
"""