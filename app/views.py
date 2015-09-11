from flask import render_template, flash, redirect
from app import app
from .forms import KeyAndSecret
from flask import request
from GetLivePlatforms import *

ResponsetoFrontEnd = "0"

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
	author = {'nickname': 'AK'} #me! 
	form = KeyAndSecret()
	if form.validate_on_submit():
		flash('Mixing Panels')
		return redirect('/result')
	return render_template('index.html', title='Home', author=author, form = form)

@app.route('/makerequest', methods=['POST'])
def handle_data():
    api_key = request.form.get('api_key')
    api_secret = request.form.get('api_secret')
    print "I see your API key is: " + api_key
    print "I see your API secret is: " + api_secret

    global ResponsetoFrontEnd
    ResponsetoFrontEnd = str(get_Mixpanel_Live_Libraries(api_key, api_secret))
    print ResponsetoFrontEnd
    return redirect('/result')

@app.route('/result')
def result():
	global ResponsetoFrontEnd
	if ResponsetoFrontEnd == "[]":
		ResponsetoFrontEnd = "no platforms found (or bad key)"
	form = KeyAndSecret()
	return render_template('result.html',livePlatforms=ResponsetoFrontEnd, form = form)	