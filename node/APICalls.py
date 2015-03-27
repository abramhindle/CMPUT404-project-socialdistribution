import urllib, urlparse, json
from urllib2 import Request, urlopen, URLError
from django.http import HttpResponse
from post.models import *
import urllib2, base64
from base64 import b64encode
import requests

def api_getPublicPost():
	url = 'http://thought-bubble.herokuapp.com/main/getposts/'
	return getJsonFromURL(url, "posts")
	
def getJsonFromURL(url, type):
	username = "admin"
	host="host"
	password="admin"
	Host= 'thought-bubble.herokuapp.com'
	try:
		Authorization = "Basic "+ base64.b64encode('%s:%s:%s' % (username,host,password)).replace('\n', '')
		headers = {'Authorization':Authorization, 'Host': Host}
		request = requests.get(url, headers=headers)

		# de-serialize the string so that we can work with it
		the_data = json.loads(request.content)

		if (the_data.get(type)):
			return the_data.get(type)
	except Exception as e:
		return HttpResponse(e.message,
                                content_type='text/plain',
                                status=500)
