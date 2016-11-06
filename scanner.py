import time
import json

from virustotal import *
from database import db
from utils import *

# global variable to terminate the run function
finished = False

# Initialize database connection
MACdb = db()

def run():
	global finished
	global MACdb

	# wrap virus total in a class
	vt = Virustotal()

	# Time the last post packet to keep the rate below per 60 seconds
	last_sending_time = -70

	while not finished:
		try:
			# Check the time elipsed since last post packet
			current_time = time.time()

			# Pause to make up for the 60 seconds interval
			if (current_time - last_sending_time) < 61 :
				time_to_sleep = 61 - current_time + last_sending_time
				print("Going to sleep for {0} to make time interval 61 seconds".format(time_to_sleep))
				time.sleep(time_to_sleep)

			# Retrieve the unscanned url from DB
			# DB will return a list of four urls
			unscanned_results = MACdb.getUnscannedResults();

			# If no current available links are available, sleep and try again
			if (len(unscanned_results) < 2):
				print("Scanner: Retrieved less than 2 entries from Database. Sleep for 10 seconds to retry.")
				time.sleep(10)
				continue

			URL_string = ""
			for each_unscanned_url in unscanned_results:
				URL_string += each_unscanned_url
				URL_string += "\n"
				MACdb.editVisitedScanEntry(each_unscanned_url, True)

			# send four urls in batch (might be less than four in case DB returns less than 4 urls)
			last_sending_time = time.time()
			website_return = vt.scanURL(URL_string)
			print("Querying following URLs:\n", URL_string)

			# Process the returned json string for each url scan
			returned_table = json.loads(json.dumps(website_return))
			for each_return in returned_table:
				print("Scanner: insertScanResultEntry({0}, {1}, {2}, {3})".format(each_return['scan_id'],each_return['url'],None, 0))
				MACdb.insertScanResultEntry(each_return['scan_id'],
											each_return['url'],
											None,
											0)
		except KeyboardInterrupt as e:
		    print "Stopping, please wait. Don't spam them Ctrl-C on me"
		    finished = True
		    MACdb.closeDB()
		    print "Exit main process."

		except:
			print("Unknown exception, continue running or Ctrl-C to stop")

if __name__ == '__main__':
	run()

