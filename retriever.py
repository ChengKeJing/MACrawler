import time
import json

from virustotal import *
from database import db

# global variable to terminate the run function
finished = False

def run():
	global finished
	
	# Initialize database connection
	MACdb = db()

	# wrap virus total in a class
	vt = Virustotal()

	# Time the last post packet to keep the rate below per 60 seconds
	last_sending_time = -70

	while not finished:

		# Check the time elipsed since last post packet
		current_time = time.time()

		# Pause to make up for the 60 seconds interval
		if (current_time - last_sending_time) < 61 :
			time.sleep(61 - current_time + last_sending_time)

		# Retrieve the unretrieved result from DB
		# DB will return four entries
		unretrieved_results = MACdb.getUnretrievedResults();
		
		# Wait for 10 seconds for scanner to insert more entries to the data base
		if(len(unretrieved_results) == 0):
			time.sleep(10)
			continue;

		HASH_ID_string = ""
		for each_unretrieved_result in unretrieved_results:
			URL_string += each_unretrieved_result.getScanID()
			URL_string += ", "

		# send four urls' Hash in batch
		last_sending_time = time.time()
		website_return = vt.rscBatchReport(URL_string)
		print("Fetching result for following URL Hashes:\n", URL_string)

		# Process the returned json string for each url scan
		returned_table = json.loads(json.dumps(website_return))
		for each_return in returned_table:
			response_code = each_return['response_code']
			
			# If the server has not finish scanning this entry, just do nothing
			# Next batch will fetch result of this url result again
			if (response_code == -2):
				continue

			# VirusTotal will return 0 for invalid url
			if (response_code == 0):
				MACdb.updateScanResultStatus(each_return['scan_id'], -1)
				continue
			
			# mark this url as retrieved
			MACdb.updateScanResultStatus(each_return['scan_id'], 1)
			is_malicious = (each_return['positives'] != 0)

			if (is_malicious):
				MACdb.updateScanResults(each_return['scan_id'], each_return['scans'])
			else:
				MACdb.updateScanResults(each_return['scan_id'], "Safe")

try:
	run()

except KeyboardInterrupt as e:
    print "Stopping, please wait. Don't spam them Ctrl-C on me"
    finished = True
    MACdb.closeDB()
    print "Exit main process."