from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class KeyAndSecret(Form):
	api_key = StringField('api_key', default="API Key", validators=[DataRequired()])
	api_secret = StringField('api_secret', default="API Secret", validators=[DataRequired()])