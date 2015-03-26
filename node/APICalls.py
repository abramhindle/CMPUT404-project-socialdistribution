import urllib, urlparse, json
from urllib2 import Request, urlopen, URLError
from django.http import HttpResponse
from post.models import *

host = 'thought-bubble.herokuapp.com'
def api_getPublicPost():
	#TODO implement calls to all allowed host apis
	#TODO if they implement authentication
	#fix this if other teams change their APIs calls
	url = 'http://' + host+ '/main/getposts/'
	return getJsonFromURL(url, "posts")
	
def getJsonFromURL(url, type):
	try:
		# download the json string
		json_string = urlopen(url).read()

		# de-serialize the string so that we can work with it
		the_data = json.loads(json_string)

		if (the_data.get(type)):
			return the_data
	except Exception as e:
		return HttpResponse(e.message,
                                content_type='text/plain',
                                status=500)
