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

			# Retrieve the unretrieved result from DB
			# DB will return four entries
			unretrieved_results = MACdb.getUnretrievedResults();
			
			# Wait for 10 seconds for scanner to insert more entries to the data base
			if(len(unretrieved_results) < 2):
				print("Retriever: Retrieved less than 2 entries from Database. Sleep for 10 seconds to retry.")
				time.sleep(10)
				continue;

			HASH_ID_string = ""
			for each_unretrieved_result in unretrieved_results:
				HASH_ID_string += each_unretrieved_result.getScanID()
				HASH_ID_string += "\n"

			# send four urls' Hash in batch
			last_sending_time = time.time()
			website_return = vt.urlReport(HASH_ID_string)
			print("Fetching result for following URL Hashes:\n{}".format(HASH_ID_string))

			# Process the returned json string for each url scan
			returned_table = json.loads(json.dumps(website_return))
			for each_return in returned_table:
				response_code = each_return['response_code']
				
				# If the server has not finish scanning this entry, just do nothing
				# Next batch will fetch result of this url result again
				if (response_code == -2):
					print("scanning for {} has not finished.".format(each_return['url']))
					continue

				# VirusTotal will return 0 for invalid url
				if (response_code == 0):
					print("updating state code of {} to -1. Server thinks this url is invalid".format(str(each_return)))
					MACdb.updateScanResultStatus(each_return['resource'], -1)
					continue
				
				# mark this url as retrieved
				print("updating status code of url {} to 1, scanning finished ".format(each_return['url']))
				MACdb.updateScanResultStatus(each_return['scan_id'], 1)
				is_malicious = (each_return['positives'] != 0)

				if (is_malicious):
					MACdb.updateScanResults(each_return['scan_id'], str(each_return['scans']))
				else:
					MACdb.updateScanResults(each_return['scan_id'], "Safe")
		
		except KeyboardInterrupt as e:
		    print "Stopping, please wait. Don't spam them Ctrl-C on me"
		    finished = True
		    MACdb.closeDB()
		    print "Exit main process."

		except:
			print("Unknown exception, continue running or Ctrl-C to stop")

if __name__ == '__main__':
	run()