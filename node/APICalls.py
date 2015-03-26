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
	getJsonFromURL(url)
	
def getJsonFromURL(url):
	try:
		# download the json string
		json_string = urlopen(url).read()

		# de-serialize the string so that we can work with it
		the_data = json.loads(json_string)


		parse_setPost(the_data)
	except Exception as e:
		return HttpResponse(e.message,
                                content_type='text/plain',
                                status=500)

def parse_setPost(jsonReply):
	hostauthor =""
	if (jsonReply.get("posts")):
		for item in jsonReply.get("posts"):
			#print(item.get('content-type') + " content-type")
			
			#maybe do some checking so the same post does not get recreated
			post = Post.objects.create(
				title=item.get('title'),
				content=item.get('content'),
				content_type=item.get('content-type'),
				#be careful of spelling
				visibility=item.get('visability'),
				guid=item.get('guid'),
				description=item.get('description'),
				origin=item.get('origin'),
				source=item.get('source'),
				pubdate=item.get('pubdate'),
				author=hostauthor
				#if (item.get('author')):
				#	author = item.get('author').get('displayname')
				#comment stuff
			)
