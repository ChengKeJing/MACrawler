"""
Helper module/script to manage
"""
import sys
from database import db

# Table names
TABLE_VISITED = 'visitedTable'
TABLE_QUEUE = 'urlQueueTable'
TABLE_RESULTS = 'scanResultTable'

def sync_table_names(db):
    db.insertTableNames(TABLE_VISITED, TABLE_RESULTS, TABLE_QUEUE)

if __name__ == '__main__':
    if cmd == 'clean-db':
        db = db()
        sync_table_names(db)
        db.deleteAllTables()
        db.createCrawlerTables(TABLE_VISITED, TABLE_RESULTS, TABLE_QUEUE)
        # Add more seeds here. The more malicious the better
        db.push('http://nus.edu.sg')
        db.closeDB()
