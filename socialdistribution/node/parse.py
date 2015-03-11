from comment.models import Comment
from post.models import Post
from author.models import FriendRequest, Author
from node.models import PostInfo


AUTHOR ="author"
POST ="post"


def setPosts(ID, type):
	"""set posts information"""
	entry = []

	if type == AUTHOR:
		#fix
		Data = Post.objects.filter(visibility = Post.PUBLIC)
		if (ID != None): 
			"""if author_id is given, return all posts the current user is
			allowed to see for that author"""
			aData = Post.objects.filter(author = ID)

	else:
		Data = Post.objects.filter(visibility = Post.PUBLIC)
		if (ID != None):
			"""return only 1 post if ID of post is given"""
			#fix -
			pData = Post.objects.filter(guid = ID)

	for post in Data:
		P = PostInfo()
		P.title = post.title
		# Todo fix
		P.source = "http://lastplaceigotthisfrom.com/post/yyyyy"
		P.origin = "http://whereitcamefrom.com/post/zzzzz"
		P.description = post.description# todo fix
		P.content_type = post.PLAIN_TEXT
		P.content = post.content
		P.author = {
			"id": str(post.author.user_id),
			"host": post.author.host,
			"displayname": post.author.github_user,
			"url": post.author.host + "/author/" + str(post.author.user_id)
		}, 
		#Todo - category not implemented yet
		P.categories = []# fix here
		comments = Comment.objects.filter(post = post)
		for c in comments:
			info = {}
			info["author"] = {
								"id": c.guid,
								"host": c.host,
								"displayname": c.displayname
							},
			info["comment"] = c.comment
			info["pubDate"] = c.pubDate
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
