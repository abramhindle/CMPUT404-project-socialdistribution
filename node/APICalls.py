import urllib, urlparse, json
from urllib2 import Request, urlopen, URLError
from django.http import HttpResponse
from post.models import *
import urllib2, base64
from base64 import b64encode
import requests
from node.models import Node
from django.contrib.auth.models import User

'''
thought-bubble.herokuapp
curl -u dan:social-distribution.herokuapp.com:dan --request GET 'http://thought-bubble.herokuapp.com/main/api/getapost/?postid=33b311fed97b11e48356005056041008'
curl -u dan:social-distribution.herokuapp.com:dan --request GET 'http://thought-bubble.herokuapp.com/main/api/getpostsbyauthor/?authorid=42567a5b-81b8-4962-a9d7-2b558b9da5c9'
curl -u dan:social-distribution.herokuapp.com:dan --request GET 'http://thought-bubble.herokuapp.com/main/api/author/posts2/'
curl -u dan:social-distribution.herokuapp.com:dan --request GET 'http://thought-bubble.herokuapp.com/main/api/getposts/'

hindlebook
http://hindlebook.tamarabyte.com/api/author/posts
http://hindlebook.tamarabyte.com/api/author/{AUTHOR_ID}/posts
curl -u team6:team6 --request GET 'http://hindlebook.tamarabyte.com/api/posts'
GET/PUT/POST
http://hindlebook.tamarabyte.com/api/post/{POST_ID}
'''
POSTS ='posts'
THOUGHTBUBBLE = 'http://thought-bubble.herokuapp.com'
HINDLEBOOK ='http://hindlebook.tamarabyte.com'

def api_getPostByAuthorID(authenticatedUser, authorID=None):
    '''get all posts visible to authenticated author'''

    nodes = Node.objects.all()

    posts = []
    for node in nodes:
    	response = None
        try:
			if 'thought-bubble' in node.host:
				if authorID is not None:
					url = THOUGHTBUBBLE +'/main/api/getpostsbyauthor/?authorid=%s' % authorID
				else:
					url = THOUGHTBUBBLE+ '/main/api/author/posts2/'
				#thoughtbubble request username for authenticatedUser
				response = requests.get(url, headers=_get_headers_thoughbubble(authenticatedUser.user.username))
			elif 'hindlebook' in node.host:
				if authorID is not None:
					url = HINDLEBOOK +'/api/author/%s/posts' % authorID
				else:
					url = HINDLEBOOK +'/api/author/posts'
				#hindlebook request uuid for authenticatedUser
				response = requests.get(url, headers=_get_headers_hindlebook(authenticatedUser.uuid))
			
			if(response !=None):
				data = json.loads(response.content)	
				if (data.get(POSTS)):
					for post in data.get(POSTS):
						posts.append(post)
        except Exception as e:
            print e.message
    return posts

def api_getPublicPost():
	'''get all public posts'''
	nodes = Node.objects.all()

	posts = []
	for node in nodes:
		response = None
		try:
			if 'thought-bubble' in node.host:
				url = THOUGHTBUBBLE + '/main/api/getposts/'
				response = requests.get(url, headers=_get_headers_thoughbubble())
			elif 'hindlebook' in node.host:
				url = HINDLEBOOK +'/api/posts'
				response = requests.get(url, headers=_get_headers_hindlebook())
		    
			if(response !=None):
				data = json.loads(response.content)	
				if (data.get(POSTS)):
					for post in data.get(POSTS):
						#add the user to our server
						if(post.get('author')):
							displayname = post.get('author').get('displayname', "")
							if 'thoughtbubble' in host:
								displayname = 'thoughtbubble'+'__'+ displayname
							if 'hindlebook' in host:
								displayname = 'hindlebook'+'__'+displayname
							uuid = post.get('author').get('id', "")
							host = post.get('author').get('host',"")
							password = 'team6'
							#add the user if they do not exist
							if len(User.objects.filter(username=displayname)) <= 0:
								user = User.objects.create_user(username=displayname,
                                                            password=password)
								Author.objects.create(user=user, host=host, uuid=uuid)
						posts.append(post)
		except Exception as e:
			print e.message
	return posts

def api_getPostByID(postID):
	'''get a post by its ID'''
	nodes = Node.objects.all()

	for node in nodes:
		try:
			response = None
			if 'thought-bubble' in node.host:
				url = THOUGHTBUBBLE+ '/main/api/getapost/?postid=%s' % (postID)
				response = requests.get(url, headers=_get_headers_thoughbubble())
			elif 'hindlebook' in node.host:
				url = HINDLEBOOK +'/api/post/%s' % postID
				response = requests.get(url, headers=_get_headers_hindlebook())

			if(response !=None):
				# de-serialize the string so that we can work with it
				data = json.loads(response.content)
				if (data.get(POSTS)):
					#only return the first post information
					return data.get(POSTS)
		except Exception as e:
			print e.message
	return None

def api_putPostByID(postObject, postID):
	'''put (update/insert) a post by its ID'''
	nodes = Node.objects.all()

	for node in nodes:
		try:
			if 'hindlebook' in node.host:
				response = requests.post('%s/api/post/%s' %(node.get_host(),
                                             postID),
                                             headers=_get_headers_hindlebook(),
                                             data=json.dumps(postObject))
			#elif 'thought-bubble' in node.host:
				#team haven't implemented yet
				#response = requests.post(node.host+ "TODO",
                                             #headers=_get_headers_thoughbubble(),
                                             #data=json.dumps(postObject))
		except Exception as e:
			print e.message
			return False

	return True

def _get_headers_thoughbubble(authenticatedUser=None):
	if(authenticatedUser == None):
		#TODO this needs to be fixed, if there is no
		#users on thoughtbubble server, it will return not authenticated
		authenticatedUser = 'dan'
	password = 'dan'
	host = 'social-distribution.herokuapp.com'
	host_url = 'thought-bubble.herokuapp.com'

	authorization = "Basic " + \
		base64.b64encode('%s:%s:%s' %
                         (authenticatedUser, host, password)).replace('\n', '')

	return {'Authorization': authorization, 'Host': host_url}

def _get_headers_hindlebook(uuid = None):
	password = 'team6'
	host = 'team6'
	host_url = 'hindlebook.tamarabyte.com'

	authorization = "Basic " + \
		base64.b64encode('%s:%s' %
                         (host, password)).replace('\n', '')

	if uuid != None:
		return {'Authorization': authorization, 'Host': host_url, 'uuid':uuid}
	return {'Authorization': authorization, 'Host': host_url}