#! /usr/bin/env python
#
# Mixpanel, Inc. -- http://mixpanel.com/
#
# Python API client library to consume mixpanel.com analytics data.
# by AK
# fearlessly debugged by Brenda!



import hashlib
import urllib
import time
from sets import Set
try:
    import json
except ImportError:
    import simplejson as json

    

def get_Mixpanel_Live_Libraries(api_keyWeb, api_secretWeb):

	class Mixpanel(object):

		ENDPOINT = 'http://mixpanel.com/api'
		VERSION = '2.0'

		def __init__(self, api_key, api_secret):
			self.api_key = api_key
			self.api_secret = api_secret
			
		def request(self, methods, params):
			"""
				methods - List of methods to be joined, e.g. ['events', 'properties', 'values']
						  will give us http://mixpanel.com/api/2.0/events/properties/values/
				params - Extra parameters associated with method
			"""
			params['api_key'] = self.api_key
			params['expire'] = int(time.time()) + 600   # Grant this request 10 minutes.

			if 'sig' in params: del params['sig']
			params['sig'] = self.hash_args(params)

			request_url = '/'.join([self.ENDPOINT, str(self.VERSION)] + methods) + '/?' + self.unicode_urlencode(params)
		
			print request_url
			
			request = urllib.urlopen(request_url)
			data = request.read()

			return data

		def unicode_urlencode(self, params):
			"""
				Convert lists to JSON encoded strings, and correctly handle any 
				unicode URL parameters.
			"""
			if isinstance(params, dict):
				params = params.items()
			for i, param in enumerate(params):
				if isinstance(param[1], list): 
					params[i] = (param[0], json.dumps(param[1]),)

			return urllib.urlencode(
				[(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params]
			)

		def hash_args(self, args, secret=None):
			"""
				Hashes arguments by joining key=value pairs, appending a secret, and 
				then taking the MD5 hex digest.
			"""
			for a in args:
				if isinstance(args[a], list): args[a] = json.dumps(args[a])

			args_joined = ''
			for a in sorted(args.keys()):
				if isinstance(a, unicode):
					args_joined += a.encode('utf-8')
				else:
					args_joined += str(a)

				args_joined += '='

				if isinstance(args[a], unicode):
					args_joined += args[a].encode('utf-8')
				else:
					args_joined += str(args[a])

			hash = hashlib.md5(args_joined)

			if secret:
				hash.update(secret)
			elif self.api_secret:
				hash.update(self.api_secret)
			return hash.hexdigest() 

	api_key = api_keyWeb  		#raw_input("API Key: ")
	api_secret = api_secretWeb	#raw_input("API Secret: ")
	api_endpoint = "live"

	currentTime = time.time()

	api = Mixpanel(
		api_key = api_key, 
		api_secret = api_secret
	)

	data = api.request([api_endpoint], {
		"start_time":currentTime
		})
	 
	#print data

	returnBlock = json.loads(data)

	output = []

	for x in returnBlock:
		y = x["properties"]	
		try: 
			if y["mp_lib"]:
				#print json.dumps(y["mp_lib"])
				output.append(json.dumps(y["mp_lib"]))
				#print "\n"
		except:
			#print "No platform found"
			print "\n"

	#print output

	myOutput = Set(output)

	finalOutput = list(myOutput)

	return finalOutput