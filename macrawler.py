from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

from forms import SearchBar
from Database import db

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
	search_form = SearchBar(csrf_enabled=False)
	domain_name = search_form.domain_name;

	if not domain_name:
		error_message = "Domain cannot be blank!"
		return render_template('index.html', error_message)
	else:
		MACdb = db()
		scan_results = MACdb.getAllScanResultsByDomain(domain_name);

		num_of_files = len(scan_results)

		MACdb.closeDB()

		return render_template('searchresults.html', num_of_files, domain_name, scan_results)