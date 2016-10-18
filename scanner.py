import postfile
import time
import os.path

from threading import Thread, RLock

# The host that Virus total server is on
host = "www.virustotal.com"

# The url of file scanner
selector = "https://www.virustotal.com/vtapi/v2/file/scan"

# API key for authentification
# Registered by @boxin
fields = [("apikey", "0cf94a0fbb09cbbd69e5e264eb24e9e1d8607157acaa25d1ad58a407022456a0")]

finished = False

def run():
	global finished
	
	file_count = 1
	last_sending_time = -20

	while not finished:
		file_name = 'file' + str(file_count)
		file_count += 1
		print "processing file ", file_name

		while (not os.path.isfile(file_name)) and (not finished):
			time.sleep(5)

		file_to_send = open(file_name, 'rb').read()
		files = [("file", file_name, file_to_send)]
		
		current_time = time.time()

		if (current_time - last_sending_time) < 15 :
			time.sleep(16 - current_time + last_sending_time)

		json = postfile.post_multipart(host, selector, fields, files)
		print json

try:
	run()

except KeyboardInterrupt as e:
    print "Stopping, please wait. Don't spam them Ctrl-C on me"
    finished = True
    print "Exit main process."