import argparse
import sys

from virustotal import Virustotal
from database import db

class VirusTotalCli:
    """ Command-line interface to retrieve scan results """

    def __init__(self):
        arg_parser = argparse.ArgumentParser(description='Command-line Interface to retrieve VirusTotal Scan results', usage='python vt-cli.py <command> [<args>]')

        arg_parser.add_argument('command', help='Subcommand to run')

        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = arg_parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print 'Unrecognized command'
            arg_parser.print_help()
            exit(1)

        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def search(self):
        """ Searches the database for a file and makes a request to the VirusTotal server for its corresponding result. """

        arg_parser = argparse.ArgumentParser(description="Searches the database for a specific file and retrieves the scan results from VirusTotal.")

        arg_parser.add_argument("file_name", help="File Name")
        arg_parser.add_argument("-v", "--verbose", action="store_true", help="Display scan results with more detail")

        # we ignore the first (main) command and parse the subcommands and its flags.
        args = arg_parser.parse_args(sys.argv[2:])

        #TODO(@jftoh) finish method to search for a specific file
    
    def list(self):
        """ Retrieves the scan results up to the last 10 files. """

        MACdb = db()
        vt_api = Virustotal()

        # retrieve all results from database
        file_list = MACdb.getAllScanResults()

        # exit program if database is empty
        if len(file_list) == 0:
            print("Database is empty.")
            exit(1)

        max_list_size = len(file_list)
        if len(file_list) > 10:
            max_list_size = 10

        # create an empty list to start appending the resource hashes
        resource_list = []

        # append the first file scan ID to the list
        resource_list.append(file_list[0].getScanID())

        if max_list_size > 1:
            # append the remaining file scan IDs to the list
            for file_details in file_list[1:max_list_size]:
                resource_list.append(', ' + file_details.getScanID())

        res_str = ''.join(resource_list)

        # Retrieve scan results using VirusTotal API in the form of a Dict
        batch_scan_results = vt_api.rscBatchReport(res_str)

        for scan_result in batch_scan_results:
            result_header = "Results for resource ID: {}".format(scan_result['resource'])
            print(result_header)
            print("="*len(result_header) + "\n")

            # print("Response Code: {}\n".format(scan_result['response_code']))

            if scan_result['response_code'] == 1:
                print("Scan Date: {}\n".format(scan_result['scan_date']))
                print("Number of positives: {}/{}\n".format(scan_result['positives'], scan_result['total']))
                print("Permalink to VirusTotal analysis: {}\n".format(scan_result['permalink']))

            elif scan_result['response_code'] == 0:
                print("Error Message: {}\n\n".format(scan_result['verbose_msg']))

            MACdb.closeDB()



if __name__ == '__main__':
    VirusTotalCli()
