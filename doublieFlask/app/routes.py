from flask import Flask
from flask import request
import urllib
import urlparse
import hashlib
app=Flask(__name__)

def parseURL():
	#makes sure that there is a url provided that can be hashed
	urlbase=request.args.get('url')
	if urlbase==None:
		raise ValueError("requires url parameter")
	
	#checks that url is first request parameter
	checkstring="url="+urlbase
	qstr=request.query_string
	if checkstring!=qstr[0:len(checkstring)]:
		raise ValueError("url should be only parameter")
	fullurl=qstr[4:]
	return fullurl

def getCheckSum(url):

	parsed=list(urlparse.urlparse(url))
	components = list(urlparse.urlparse(url))
	parameters = list(urlparse.parse_qsl(components[4]))
	checksum=hashlib.sha1(url).hexdigest()
	
	if len(query)>0:
		url+="&"
	else:
		url+="?"
	url+="checksum="
	url+=checksum
	return url


#root route will be treated as creating checksum
@app.route('/')
@app.route('/createchecksum')
def home():
	try:
		url=parseURL()
	except ValueError as err:
		return tuple([err.args, 400])	
	try:
		modifiedurl=getCheckSum(url)
	except ValueError as err:
		return tuple([err.args, 400])
	return modifiedurl

@app.route('/checkchecksum')
def verify():
	#retrieving url excluding checksum
	qstr=request.query_string
	cs=qstr.index("checksum=")
	url=qstr[4:cs-1]

	#retrieving checksum variable from url
	url_parts = list(urlparse.urlparse(qstr[4:]))
	query = dict(urlparse.parse_qs(url_parts[4]))
	checksum=query['checksum'][0]

	#comparing calculated checksum to given checksum
	if checksum!=str(hashlib.sha1(url).hexdigest()):
		return tuple(["not verified", 400])
	return "verified"


if __name__=='__main__':
	app.run(debug=True)
	#create key here

