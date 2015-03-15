from comment.models import Comment
from post.models import *
from author.models import FriendRequest, Author
from node.models import PostInfo


AUTHOR ="author"
POST ="post"


def setPosts(request, ID, type):
	"""set posts information"""
	entry = []

	if type == AUTHOR:
		if request.user.is_authenticated():
			currentAuthor = Author.objects.get(user=request.user)
			Data = Post.getVisibleToAuthor(currentAuthor)
			if (ID != None): 
				"""if author_id is given, return all posts the current user is
				allowed to see for that author"""
				#fix- needs a diff method for this
				Data = Post.getVisibleToAuthor(ID)
		else:
			return ""
	else: 
		"""POST"""
		Data = Post.objects.filter(visibility = Post.PUBLIC)
		if (ID != None):
			"""return only 1 post if ID of post is given"""
			Data = Post.objects.filter(guid = ID)

	for post in Data:
		P = PostInfo()
		P.title = post.title
		# Todo fix //no clue...
		P.source = "http://lastplaceigotthisfrom.com/post/yyyyy"
		P.origin = "http://whereitcamefrom.com/post/zzzzz"
		P.description = post.description
		P.content_type = post.content_type
		P.content = post.content
		P.author = {
			"id": str(post.author.user_id),
			"host": post.author.host,
			"displayname": post.author.github_user,
			"url": post.author.host + "/author/" + str(post.author.user_id)
		}, 
		#Todo - category not implemented yet
		P.categories = []
		comments = Comment.objects.filter(post = post)
		for c in comments:
			info = {}
			info["author"] = {
								"id": c.guid,
								"host": c.author.host,
								"displayname": c.author.user.username
							},
			#LOOK INTO- c.comment is not working for author post lookup
			#returns all the items in comment
			info["comment"] = c.comment
			info["pubDate"] = str(c.pubDate)
			info["guid"] = c.guid
			P.comments.append(info)
		P.pubDate = str(post.publication_date)
		P.guid = post.guid
		P.visibility = post.visibility

		# add to entry post items
		entry.append(P)

	results = {}
	results["post"] = entry
	return results
