import urllib, urlparse, json
from urllib2 import Request, urlopen, URLError
from django.http import HttpResponse
from post.models import *

def api_getPublicPost():
	#TODO implement calls to all allowed host apis
	#TODO if they implement authentication
	#fix this if other teams change their APIs calls
    url = 'http://thought-bubble.herokuapp.com/main/getposts/'
    url = url_fix(url)
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
	if (jsonReply.get("posts")):
		for item in jsonReply.get("posts"):
			#print(item.get('content-type') + " content-type")
			post = Post.objects.create(
					title=item.get('title'),
					content=item.get('content'),
					content_type=item.get('content-type'),
					visibility=item.get('visibility'),
					guid=item.get('guid'),
					description=item.get('description'),
					origin=item.get('origin'),
					source=item.get('source'),
					pubdate=item.get('pubdate'),
					#receive_author=Author.objects.get(user=User.objects.get(username=receive_author)),
					#comments
			)
			post.save()
    
def url_fix(s, charset='utf-8'):
    '''Sometimes you get an URL by a user that just isn't a real
    URL because it contains unsafe characters like ' ' and so on.  This
    function can fix some of the problems in a similar way browsers
    handle data entered by the user:
    :param charset: The target charset for the URL if the url was
                    #given as unicode string.
    '''
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))