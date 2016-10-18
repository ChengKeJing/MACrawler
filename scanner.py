import time
import os.path

from virustotal import *

finished = False

def run():
	global finished
	
	v = Virustotal()
	file_count = 1
	last_sending_time = -20

	while not finished:
		file_name = 'file' + str(file_count)
		file_count += 1
		print "processing file ", file_name

		while (not os.path.isfile(file_name)) and (not finished):
			time.sleep(5)
		
		current_time = time.time()

		if (current_time - last_sending_time) < 15 :
			time.sleep(16 - current_time + last_sending_time)

		last_sending_time = time.time()
		json = v.rscSubmit(file_name)
		## TODO(ChengKeJing) : extract useful information and store it into database
		## TODO(boxin) : solve the server error and crawl and parse the analysis result
		print json

try:
	run()

except KeyboardInterrupt as e:
    print "Stopping, please wait. Don't spam them Ctrl-C on me"
    finished = True
    print "Exit main process."