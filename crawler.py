import random
import time
from Queue import Queue
from threading import Thread, RLock
from urlparse import urlparse, urljoin

import requests
from HTMLParser import HTMLParser

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

class Crawler:
    """The class responsible to do the crawling"""

    # For file naming
    file_count = 0

    # Prevent race condition and whatnot when reading/incrementing file_count
    file_count_lock = RLock()

    # To accept interrupt
    stopped = False

    ##
    ## @brief      Gets the file count, which is used for file name identifier.
    ##
    ## @return     The file count.
    ##
    @staticmethod
    def get_file_count():
        with Crawler.file_count_lock:
            Crawler.file_count += 1
            return Crawler.file_count

    ##
    ## @brief      Constructor.
    ##
    ## @param      self   The object
    ## @param      url_q  The url Queue from which the Crawler retrieve and
    ##                    store URLs from/to
    ##
    def __init__(self, url_q):
        self.url_q = url_q

    ##
    ## @brief      Runs the crawler.
    ##
    ## @param      self  The object
    ##
    def run(self):
        while not Crawler.stopped:
            # TODO(@digawp): handle case when the url_q is really empty (and no
            # one else is going to replenish it)
            # NOTE: use a wrapper for the queue, timeout, try-catch
            url = self.url_q.get()
            print 'Visiting {}'.format(url)

            response = requests.get(url)
            parsed_url = urlparse(url)
            print 'Content-Type: ', response.headers['Content-Type']

            if 'text' not in response.headers['Content-Type']:
                out = open('file'+str(Crawler.get_file_count()), 'wb')
                out.write(response.content)
                out.close()
            else:
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
                    self.url_q.put(obtained_url)
            print "Sleeping..."
            time.sleep(random.randint(5,15))

def run_crawler(q):
    crawler = Crawler(q)
    crawler.run()

if __name__ == '__main__':
    q = Queue()
    q.put('http://www.comp.nus.edu.sg')

    threads = []
    for i in range(0,3):
        t = Thread(target=run_crawler, args=[q])
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
