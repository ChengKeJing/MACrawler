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
    db.push('http://musicpleer.cc/')
    db.push('https://sourceforge.net/')
    db.push('http://thepiratebay.org/')
    db.push('http://download.cnet.com/')
    db.push('http://www.msconline.com/')
    db.push('http://www.airdental.es/')
    db.push('http://comp.nus.edu.sg/')
    db.closeDB()
