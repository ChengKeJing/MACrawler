import time
import json

from virustotal import *
from database import db

# global variable to terminate the run function
finished = False

# Initialize database connection
MACdb = db()

def run():
	global finished
	
	# wrap virus total in a class
	vt = Virustotal()

	# Time the last post packet to keep the rate below per 60 seconds
	last_sending_time = -70

	# Create DB table to store the scanning result
	MACdb.createScanResultTable("scanResults")

	while not finished:

		# Check the time elipsed since last post packet
		current_time = time.time()

		# Pause to make up for the 60 seconds interval
		if (current_time - last_sending_time) < 61 :
			time.sleep(61 - current_time + last_sending_time)

		# Retrieve the unscanned result from DB
		# DB will return four entries
		unscanned_results = MACdb.getUnscannedResults();
		URL_string = ""
		for each_unscanned_result in unscanned_results:
			URL_string += each_unscanned_result.getURL()
			URL_string += "\n"

		# send four urls in batch
		last_sending_time = time.time()
		website_return = vt.scanURL(URL_string)
		print("Querying following URLs:\n", URL_string)

		# Process the returned json string for each url scan
		returned_table = json.loads(json.dumps(website_return))
		for each_return in returned_table:
			MACdb.insertScanResultEntry(each_return['scan_id'],
										each_return['url'],
										None,
										each_return['response_code'])

		# Store in the data base the hash and url
		id_of_the_file = returned_table['scan_id']
		link_to_result = returned_table['permalink']
		print "id of the file is : ", id_of_the_file, "\nlink to the result is: ", link_to_result, "\n"

		## Extract useful information and store it into database
		MACdb.insertScanResult("scanResults", file_name, id_of_the_file, link_to_result)

try:
	run()

except KeyboardInterrupt as e:
    print "Stopping, please wait. Don't spam them Ctrl-C on me"
    finished = True
    MACdb.closeDB()
    print "Exit main process."