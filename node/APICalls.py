import urllib, urlparse, json
from urllib2 import Request, urlopen, URLError
from django.http import HttpResponse
from post.models import *
import urllib2, base64
from base64 import b64encode
import requests

'''
thought-bubble.herokuapp
curl -u admin:host:admin --request GET 'http://thought-bubble.herokuapp.com/main/getapost/?postid=37c1792353234b90abe6f4c9e316fab8'
curl -u admin:host:admin --request GET 'http://thought-bubble.herokuapp.com/main/getauthorposts/?authorid=3cf3d542f96a42c3a8edd5da02826740/'
curl -u admin:host:admin --request GET 'http://thought-bubble.herokuapp.com/main/author/posts2/'
curl -u admin:host:admin --request GET 'http://thought-bubble.herokuapp.com/main/getposts/'
'''
POSTS ='posts'

def api_getPostByAuthorID(authenticatedUser, authorID=None):
    '''get all posts visible to authenticated author'''
    if authorID is not None:
        url = 'http://thought-bubble.herokuapp.com/main/getauthorposts/?authorid=%s' % authorID
    else:
        url = 'http://thought-bubble.herokuapp.com/main/author/posts2/'

    data = getJsonFromURL(url, authenticatedUser)
    if (data.get(POSTS)):
        return data.get(POSTS)
    return ""

def api_getPostByID(postID):
	'''get a post by its ID'''
	url = 'http://thought-bubble.herokuapp.com/main/getapost/?postid=%s' % postID
	
	data = getJsonFromURL(url)
	if (data.get(POSTS)):
		return data.get(POSTS)
	return ""

def api_getPublicPost():
	'''get all public posts'''
	url = 'http://thought-bubble.herokuapp.com/main/getposts/'

	data = getJsonFromURL(url)
	if (data.get(POSTS)):
		return data.get(POSTS)
	return ""
	
def getJsonFromURL(url, user=None):
	username = "admin"
	if(user !=None):
		username=user
	host="host"
	password="admin"
	Host= 'thought-bubble.herokuapp.com'
	try:
		Authorization = "Basic "+ base64.b64encode('%s:%s:%s' % (username,host,password)).replace('\n', '')
		headers = {'Authorization':Authorization, 'Host': Host}
		request = requests.get(url, headers=headers)

		# de-serialize the string so that we can work with it
		the_data = json.loads(request.content)
		return the_data
	except Exception as e:
		return HttpResponse(e.message,
                                content_type='text/plain',
                                status=500)
