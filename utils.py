"""
Helper module/script to manage initialization of db
"""
import sys
from database import db

if __name__ == '__main__':
    db = db()
    db.deleteAllTables()
    db.createCrawlerTables()
    # Add seeds here. The more malicious the better
    db.push('http://nus.edu.sg/')
    db.push('http://comp.nus.edu.sg/')
    db.push('http://www.github.com/')
    db.push('http://www.msconline.com/')
    db.push('http://tvstreamtimes.co/')
    db.push('http://www.szxx.com.cn/')
    db.push('http://www.bokepnews.com/')
    db.push('http://www.airdental.es/')
    db.closeDB()
