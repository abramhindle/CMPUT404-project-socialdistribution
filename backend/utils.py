from rest_framework import status
from rest_framework.response import Response
from manager.settings import HOSTNAME
from .models import Author, Follow, Like, Node, Post, Comment, Node, Inbox
from .serializers import FollowSerializer, LikeSerializer, PostSerializer

import json


def get_author_by_ID(request, author_id, label):
	"""
	This function takes a request object and author ID as parameters, it will check if the author is in our database and add the author if it is not. Returns the author object and a boolean representing if it is local or remote.
	"""

	# Decode the request body and load into a json
	body = json.loads(request.body.decode('utf-8'))

	# Check if the foreign ID exists in the database, if not add that Author to our database
	try:
		author = Author.objects.filter(id=author_id).get()
		if HOSTNAME in author.host :
			return author, True
		else:
			return author, False
	except Exception as e:
		node = Node.objects.filter(host__icontains=body[label]["host"]).get()
		author = Author(
			id = author_id,
			user = node.user,
			displayName = body[label]["displayName"],
			github = body[label]["github"],
			host = body[label]["host"],
			url = body[label]["url"]
		)
		author.save()
		return author, False


def add_post(request, author,id=None):

	body = json.loads(request.body.decode('utf-8'))

	try:
		post = Post.objects.filter(id=id).get()
		return post, PostSerializer(post, remove_fields={'size'}).data, True
	except:
		pass

	if id:
		post = Post(
			id = id,
			author = author,
			title = body["title"],
			host = HOSTNAME,
			source = body["source"],
			origin = body["origin"],
			description = body["description"],
			contentType = body["contentType"],
			categories = body["categories"],
			visibility = body["visibility"],
			unlisted = body["unlisted"]
		)
	else:
		post = Post(
			author = author,
			title = body["title"],
			host = HOSTNAME,
			description = body["description"],
			contentType = body["contentType"],
			categories = body["categories"],
			visibility = body["visibility"],
			unlisted = body["unlisted"]
		)

	if any([types in body["contentType"] for types in ['application/base64', 'image/png', 'image/jpeg']]):
		post.image_content = body["content"]
	# If the post does not contain image content
	else:
		post.content = body["content"]

	post.save()

	return post, PostSerializer(post, remove_fields={'size'}).data, False


def get_objects_by_ID(authorID, user=None,postID=None, commentID=None):

	author = None
	post = None
	comment = None

	if user:
		author = Author.objects.filter(user=user, id=authorID)

		if not author:
			raise Exception("User forbidden")
		else:
			author = author.get()


	else:
		author = Author.objects.filter(id=authorID)

		if not author:
			raise Exception("Author object not found")
		else:
			author = author.get()

	if postID:
		post = Post.objects.filter(id=postID)
		if not post:
			raise Exception("Post object not found")
		else:
			post = post.get()

		if post.author.id != author.id:
			raise Exception("Author does not match post")

	if commentID:
		comment = Comment.objects.filter(id=commentID)

		if not comment:
			raise Exception("Comment object not found")
		else:
			comment = comment.get()

		if post.id != comment.post.id:
			raise Exception("Comment not on post")


	return author, post, comment



def get_object_data(request, label):

	body = json.loads(request.body.decode('utf-8'))

	dataList = body[label].split("/")
	author = None
	post = None
	comment = None

	for i in range(len(dataList)):

		if dataList[i] == "author":
			author = Author.objects.filter(id=dataList[i+1])
			if not author:
				raise Exception("Author object not found")
			else:
				author = author.get()

		elif dataList[i] == "posts":
			post = Post.objects.filter(id=dataList[i+1])
			if not post:
				raise Exception("Post object not found")
			else:
				post = post.get()

			if post.author.id != author.id:
				raise Exception("Author does not match post")

		elif dataList[i] == "comments":
			comment = Comment.objects.filter(id=dataList[i+1])

			if not comment:
				raise Exception("Comment object not found")
			else:
				comment = comment.get()

			if post.id != comment.post.id:
				raise Exception("Comment not on post")


	return author, post, comment


def add_like(request, like_author, object_author, object, label):

	if label == "post":
		like = Like(
		post=object,
		author=like_author,
		summary=like_author.displayName+" Likes your post"
		)
	else:
		like = Like(
		comment=object,
		author=like_author,
		summary=like_author.displayName+" Likes your comment"
		)

	inbox = Inbox(
		author=object.author,
		like=like
	)
	like.save()
	inbox.save()

	return like, LikeSerializer(like, context={'request': request}).data

def add_follow(object_author, actor_author):
	# Check if the follow already exists
	if Follow.objects.filter(follower=actor_author, followee=object_author):
		raise Exception("Follow already exists"+str(actor_author.displayName)+str(object_author.displayName))

	# Check if the follower is already being followed by the followee
	reverse_follow = Follow.objects.filter(follower=object_author, followee=actor_author)
	# Create the follow
	follow = Follow(
				follower=actor_author,
				followee=object_author,
				summary=actor_author.displayName + " wants to follow " + object_author.displayName
				)
	# If a follow does exist then set their relationship as being friends and create a follow
	if reverse_follow:
		follow.friends = True
		reverse_follow.update(friends=True)
	follow.save()

	return follow, FollowSerializer(follow).data, reverse_follow

def add_comment(request, comment_author, post):

	body = json.loads(request.body.decode('utf-8'))

	# Create the comment object in the database:
	idData = body["id"].split('/')

	for i in range(len(idData)):
		if idData[i] == "comments":
			commentID = idData[i+1]

	comment = Comment(
		id = commentID,
		author = comment_author,
		post = post,
		comment = body["comment"],
		contentType = body["contentType"],
		host = HOSTNAME,
		post_author = post.author,
	)
	comment.save()

	return comment

def send_to_remote(data):
	pass