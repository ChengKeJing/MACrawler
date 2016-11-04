from flask_wtf import FlaskForm
from wtforms import StringField

class SearchBar(FlaskForm):
	domain_name = StringField('domain_name')