import argparse
import sys

from virustotal import Virustotal
from database import db


class VirusTotalCli:
    """ Command-line interface to retrieve scan results """

    def __init__(self):
        arg_parser = argparse.ArgumentParser(description='Command-line Interface to retrieve VirusTotal Scan results',
                                             usage='python vt-cli.py <command> [<args>]')

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

    def list(self):
        """ Retrieves the scan results for the first 8 files. """

        # initialize postgreSQL database and VirusTotal API
        MACdb = db()
        vt_api = Virustotal()

        # retrieve all results from database
        file_list = MACdb.getAllScanResults()

        max_list_size = len(file_list)

        # exit program if database is empty
        if max_list_size == 0:
            print("Database is empty.")
            exit(1)

        if len(file_list) > 8:
            max_list_size = 8

        # create an empty list to start appending the resource hashes
        resource_list = []

        out_file = open("scanresults.txt", "w")

        for i in range(0, max_list_size + 1):
            # append the first file scan ID to the list
            if i == 0:
                resource_list.append(file_list[i].getScanID())
            else:
                # append the remaining file scan IDs to the list
                resource_list.append(', ' + file_list[i].getScanID())

            if len(resource_list) == 4:
                """ we send the batch to VirusTotal when the file count reaches 4 """
                res_str = ''.join(resource_list)

                # Retrieve scan results using VirusTotal API in the form of a Dict
                print("Sending file batch...\n")
                batch_scan_results = vt_api.rscBatchReport(res_str)

                for scan_result in batch_scan_results:
                    write_scan_result(scan_result, out_file)

                print("Results for current batch successfully written to file {}.\n\n".format(out_file.name))

                # clears the resource list for the next batch of scan IDs
                resource_list = []

        # close the database when done
        MACdb.closeDB()

        out_file.close()


def write_scan_result(scan_result, out_file):
    """ Writes the current scan result to a text file. """

    result_header = "Results for resource ID: {}".format(scan_result['resource'])
    out_file.write(result_header)
    out_file.write("=" * len(result_header) + "\n")

    # print("Response Code: {}\n".format(scan_result['response_code']))

    if scan_result['response_code'] == 1:
        out_file.write("Scan Date: {}\n".format(scan_result['scan_date']))
        out_file.write("Number of positives: {}/{}\n".format(scan_result['positives'], scan_result['total']))
        out_file.write("Permalink to VirusTotal analysis: {}\n\n".format(scan_result['permalink']))

    elif scan_result['response_code'] == 0:
        out_file.write("Error Message: {}\n\n".format(scan_result['verbose_msg']))

    elif scan_result['response_code'] == -2:
        out_file.write(scan_result['verbose_msg'] + "\n\n")


if __name__ == '__main__':
    VirusTotalCli()
