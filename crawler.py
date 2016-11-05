import random
import time
from Queue import Queue
from threading import Thread, RLock
from urlparse import urlparse, urljoin

import requests
from HTMLParser import HTMLParser

import database
import utils

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.urls = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag.encode('utf-8') is 'a':
            self.want_data = True
            for attr in attrs:
                if attr[0].encode('utf-8') == 'href':
                    self.urls.append(attr[1].encode('utf-8'))

##
## @brief      Simulate enum type in Python 2
##
## Usage: UrlType.PAGE
## The above returns 0.
##
class UrlType:
    PAGE, FILE = range(2)

class Crawler:
    """The class responsible to do the crawling"""

    # To accept interrupt
    stopped = False

    ##
    ## @brief      Constructor.
    ##
    ## @param      self   The object
    ## @param      url_q  The url Queue from which the Crawler retrieve and
    ##                    store URLs from/to
    ##
    def __init__(self):
        self.db = database.db()
        utils.sync_table_names(self.db)

    ##
    ## @brief      Runs the crawler.
    ##
    ## @param      self  The object
    ##
    def run(self):
        while not Crawler.stopped:
            print "Sleeping..."
            time.sleep(random.randint(5,15))
            # TODO(@digawp): handle case when the url_q is really empty (and no
            # one else is going to replenish it)
            url = ''
            try:
                url = self.db.pop()
                print 'Visiting {}'.format(url)
            except Exception as e:
                print(e)
                print 'Probably empty table. Continue...'
                continue

            response = requests.get(url)
            print 'Content-Type: ', response.headers['Content-Type']

            if 'text' not in response.headers['Content-Type']:
                parsed_url = urlparse(url)
                self.db.insertVisitedEntry(url, UrlType.FILE, url[1])
            else:
                self.db.insertVisitedEntry(url, UrlType.PAGE, url[1])
                parser = MyHTMLParser()
                parser.feed(response.text)
                for obtained_url in parser.urls:
                    parsed_obtained_url = urlparse(obtained_url)

                    # Skip non-http URLs
                    if 'http' not in parsed_obtained_url[0]:
                        continue

                    # If netloc is empty (i.e. relative URL)
                    if parsed_obtained_url[1] == '':
                        obtained_url = urljoin(url, obtained_url)

                    # print 'Pushing {} to url_q'.format(obtained_url)
                    if not self.db.isVisited(obtained_url):
                        self.db.push(obtained_url)
        self.db.closeDB()



def run_crawler():
    crawler = Crawler()
    crawler.run()

if __name__ == '__main__':
    threads = []
    for i in range(0,3):
        t = Thread(target=run_crawler)
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(0.5)

    except KeyboardInterrupt as e:
        print "Stopping, please wait. Don't spam them Ctrl-C on me"
        Crawler.stopped = True
        for i in range(0,3):
            threads[i].join()
        print "All threads exited. Exit main process."
