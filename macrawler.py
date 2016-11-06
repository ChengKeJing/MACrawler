from flask import Flask, render_template, request, url_for
app = Flask(__name__)

import utils
from database import db

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search')
def search():
	domain_name = request.args.get('domain_name', '')

	if not domain_name:
		error_message = "Domain cannot be blank!"
		return render_template('index.html', error_message=error_message)
	else:
		MACdb = db()
		# utils.sync_table_names(MACdb)

		scan_results = MACdb.getAllScanResultsByDomain(domain_name);

		num_of_files = len(scan_results)

		MACdb.closeDB()

		return render_template('searchresults.html', num_of_files=num_of_files, domain_name=domain_name, scan_results=scan_results)

@app.route('/detailed/<string:scan_id>')
def detailed(scan_id, scans):
	return render_template('detailedresults.html', scan_id=scan_id, scans=scans)