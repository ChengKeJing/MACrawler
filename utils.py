"""
Helper module/script to manage
"""
import sys
from database import db

# Table names
TABLE_VISITED = 'visitedTable'
TABLE_QUEUE = 'urlQueueTable'
TABLE_RESULTS = 'scanResultTable'

##
## @brief      Used to ensure the db class use the same table names across all
##             the different modules
##
## @param      db    The database class
##
def sync_table_names(db):
    db.insertTableNames(TABLE_VISITED, TABLE_RESULTS, TABLE_QUEUE)

if __name__ == '__main__':
    if sys.argv[1] == 'clean-db':
        db = db()
        sync_table_names(db)
        db.deleteAllTables()
        db.createCrawlerTables(TABLE_VISITED, TABLE_RESULTS, TABLE_QUEUE)
        # Add seeds here. The more malicious the better
        db.push('http://nus.edu.sg')
        db.push('http://comp.nus.edu.sg')
        db.push('http://www.github.com')
        db.push('http://www.msconline.com')
        db.push('http://tvstreamtimes.co')
        db.push('http://www.szxx.com.cn')
        db.push('http://www.bokepnews.com')
        db.push('http://www.airdental.es')
        db.closeDB()
