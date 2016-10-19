import time
import os.path
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
	v = Virustotal()

	# Counter for file names
	file_count = 1

	# Time the last post packet to keep the rate below per 15 seconds
	last_sending_time = -20

	# Delete old table and recreate new one
	MACdb.deleteTable("scanResults")
	MACdb.createScanResultTable("scanResults")

	while not finished:
		
		# Following the file names from crawler.py
		file_name = 'file' + str(file_count)
		file_count += 1
		print "processing :", file_name

		# If the file is not found, wait for the crawler to generate more files
		while (not os.path.isfile(file_name)) and (not finished):
			time.sleep(5)
		
		# Check the time elipsed since last post packet
		current_time = time.time()

		# Pause to make up for the 15 seconds interval
		if (current_time - last_sending_time) < 15 :
			time.sleep(16 - current_time + last_sending_time)

		# second post packet
		last_sending_time = time.time()
		website_return = v.rscSubmit(file_name)

		# Process the returned json string
		returned_table = json.loads(json.dumps(website_return))

		# code 1 means success
		response_code = returned_table['response_code']
		if (response_code != 1):
			continue

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