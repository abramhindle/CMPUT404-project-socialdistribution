from manager.settings import HOSTNAME
from manager.paginate import ResultsPagination
from ..models import Author, Comment, Follow, Inbox, Like, Post, Node
from ..serializers import CommentSerializer, FollowSerializer, LikeSerializer, PostSerializer

import requests
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from .. import utils

import json

class InboxAPI(viewsets.ModelViewSet):
	"""
	This class specifies the view for the a list of Likes by an Author. This will run methods to retrieve DB rows and return correctly formatted HTTP responses
	"""

	# Specifies the permissions required to access the data
	permission_classes = [
		permissions.IsAuthenticated
	]

	# Specifies the field used for querying the DB
	lookup_field = 'id'

	# Specifies the serializer used to return a properly formatted JSON response body
	serializer_class = FollowSerializer

	# Specifies the query set of Post objects that can be returned
	queryset = Inbox.objects.all()

	def list(self, request, author_id=None, *args, **kwargs):

		# Try to get the author object referenced in the request URL, return a 404 if it is not found
		try:
			check_author = Author.objects.filter(id=author_id).get()
		except:
			return Response(status=status.HTTP_404_NOT_FOUND, data="Unable to find the author who's inbox this is!")

		# Check that the authenticated user making the request is the author who's inbox it is, otherwise return a 403 Forbidden
		if request.user.is_authenticated and (check_author.user == request.user):

			# Check that the author id is found in the url, otherwise return a 400
			if author_id:
				# Set the pagination class for the results of this method
				self.pagination_class = ResultsPagination

				# Find follows, posts, likes, and comments from the inbox table that belong to this author
				follows_list = Inbox.objects.filter(author=author_id, follow__isnull=False)
				posts_list = Inbox.objects.filter(author=author_id, post__isnull=False)
				likes_list = Inbox.objects.filter(author=author_id, like__isnull=False)
				comments_list = Inbox.objects.filter(author=author_id, icomment__isnull=False)

				# Find the full follow, post, like, and comment objects in their respective tables
				follows = Follow.objects.filter(follow__in=follows_list)
				posts = Post.objects.filter(post__in=posts_list)
				likes = Like.objects.filter(like__in=likes_list)
				comments = Comment.objects.filter(comment__in=comments_list)

				# Serialize the returned rows from each table
				post_serializer = PostSerializer(posts, many=True, remove_fields={'size'})
				follow_serializer = FollowSerializer(follows, many=True)
				like_serializer = LikeSerializer(likes, many=True, context={'request': request})
				comment_serializer = CommentSerializer(comments, many=True)

				# Paginate the returned data from all of the serializers
				paginated_serializer_data = self.paginate_queryset(follow_serializer.data+like_serializer.data+post_serializer.data+comment_serializer.data)

				# Return the inbox
				return Response({
					"type":"inbox",
					"author":HOSTNAME+"author/"+author_id,
					"items": paginated_serializer_data
				})
			else:
				return Response(status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def create(self, request, author_id=None, *args, **kwargs):

		# Check if the inbox owner is a valid author on our server
		try:
			inbox_author = Author.objects.filter(id=author_id).get()
		except:
			return Response(data="URL author not found",status=status.HTTP_404_NOT_FOUND)
		# Check that the author ID is for a valid author
		try:
			author = Author.objects.filter(id=author_id).get()
		except:
			return Response(status=status.HTTP_404_NOT_FOUND)
		# Check that the request body is valid
		try:
			body = json.loads(request.body.decode('utf-8'))
		except:
			return Response(data="Not a valid request body!", status=status.HTTP_400_BAD_REQUEST)

		# If the sent object is of type Follow
		if body['type'].lower() == 'follow':

			# Get the actor author information
			try:
				actor_author, isLocal = utils.get_author_by_ID(request, body['actor']['id'].split("/")[-1], "actor")
			except Exception as e:
				return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
			# Get the object author information
			try:
				object_author, isLocal = utils.get_author_by_ID(request, body['object']['id'].split("/")[-1], "object")
			except Exception as e:
				return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)

			# Check if author ID is matching
			if object_author.id != inbox_author.id:
				return Response(data="Author doesn't match request followee", status=status.HTTP_400_BAD_REQUEST)

			# Get the follow object and the serialized data
			try:
				follow, follow_data, reverse_follow = utils.add_follow(inbox_author, actor_author)
			except Exception as e:
				return Response(data=str(e), status=status.HTTP_409_CONFLICT)

			# Add this follow to the inbox of the author ID provided
			inbox = Inbox(
				author=inbox_author,
				follow=follow
			)
			inbox.save()
			# Return the follow object
			return Response(data="Follow sent to inbox", status=status.HTTP_201_CREATED)
		# If the sent object is of type Like
		elif body['type'].lower() == 'like':

			# Parse the input object and author ID
			object_data = body['object'].split('/')
			like_author_data = body['author']['id'].split('/')
			# Parse the data and return an author, post and comment object
			try:
				object_author, post, comment = utils.get_object_data(request, "object")
			except Exception as e:
				return Response(data=str(e), status=status.HTTP_404_NOT_FOUND)

			try:
				comment_author, isLocal = utils.get_author_by_ID(request, body["author"]["id"].split('/')[-1], "author")
			except Exception as e:
				return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)

			# Check if the post/comment creator is the same as the inbox recipient
			if object_author.id != inbox_author.id and comment_author.id != inbox_author.id:
				return Response(data="Creator does not match inbox owner", status=status.HTTP_400_BAD_REQUEST)
			# Get the like author and if they are local or remote
			try:
				like_author, isLocal = utils.get_author_by_ID(request, like_author_data[-1], "author")
			except Exception as e:
				return Response(data=str(e), status=status.HTTP_404_NOT_FOUND)
			# If the like is on a Post
			if comment is None:
				# Check that the author of the post is the one receiving the like
				if post.author.id == author_id:
					# Check if the like already exists
					if not Like.objects.filter(author=like_author, post=post):
						# Create the like and send to their inbox
						try:
							like, like_data = utils.add_like(request, like_author, object_author, post, "post")
						except Exception as e:
							return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
					else:
						return Response(data="Like already exists for this post", status=status.HTTP_409_CONFLICT)
			# If the like is on a Comment
			else:
				# Check that the author of the comment is the one receiving the like
				if comment.author.id == author_id:
					# Check if the like already exists
					if not Like.objects.filter(author=like_author, comment=comment):
						# Create the like and send to their inbox
						try:
							like, like_data = utils.add_like(request, like_author, object_author, comment, "comment")
						except Exception as e:
							return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
					else:
						return Response(data="Like already exists for this post", status=status.HTTP_409_CONFLICT)

			# Check if the request needs to be sent to a remote server
			try:
				node = Node.objects.filter(host__icontains=object_author.host).get()
			except:
				pass
			else:
				s = requests.Session()
				s.auth = (node.remote_username, node.remote_password)
				s.headers.update({'Content-Type':'application/json'})
				url = node.host+"author/"+object_author.id+"/inbox"
				if 'konnection' in node.host:
					url += '/'
				response_like = s.post(url, json=like_data)

				if not response_like.status_code in [200, 201]:
					like.delete()
					return Response(data="Like not accepted by remote host", status=status.HTTP_400_BAD_REQUEST)

			# Respond with a 201 created
			return Response(data="Like sent to inbox", status=status.HTTP_201_CREATED)

		# If the sent object is of type Post
		elif body['type'].lower() == 'post':
			# Get or create a local copy of the author of the post
			try:
				post_author, isLocal = utils.get_author_by_ID(request, body['author']['id'].split('/')[-1], "author")
			except Exception as e:
				return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
			# Get or create a local copy of the post
			try:
				post, post_data, exists = utils.add_post(request, post_author, body['id'].split('/')[-1])
			except Exception as e:
				return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
			# Add the post to the inbox
			try:
				inbox = Inbox(
					author=inbox_author,
					post=post
				)
				inbox.save()
			except Exception as e:
					return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
			# Respond with a 201 created
			return Response(data="Post sent to inbox",status=status.HTTP_201_CREATED)

		# If the sent object is of type Comment
		elif request.data['type'].lower() == 'comment':
			# Get the post author, post and comment
			try:
				post_author, post, comment = utils.get_object_data(request, "id")
			except Exception as e:
				return Response(data=str(e), status=status.HTTP_404_NOT_FOUND)
			# Get the author of the comment if they exist
			try:
				comment_author, isLocal = utils.get_author_by_ID(request, body["author"]["id"].split('/')[-1], "author")
			except Exception as e:
				return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
			# Check if the author of the post is the recipient of the inbox item
			if comment_author.id != inbox_author.id:
				return Response(data="Creator does not match inbox owner", status=status.HTTP_400_BAD_REQUEST)
			# If a comment does not exist locally
			if comment is None:
				try:
					comment, comment_data = utils.add_comment(request, comment_author, post)
				except Exception as e:
					return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
			# Create an inbox item
			try:
				inbox = Inbox(
					author=inbox_author,
					icomment=comment
				)
				inbox.save()
			except Exception as e:
					return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
			# Respond that the comment was created with a 201
			return Response(data="Comment sent to inbox", status=status.HTTP_201_CREATED)

	def destroy(self, request, author_id=None, *args, **kwargs):
		"""
		This method clears the inbox for the author ID provided as argument.
		"""
		# Check if the author exists
		try:
			author = Author.objects.filter(id=author_id).get()
		except:
			return Response(data="Author does not exists", status=status.HTTP_404_NOT_FOUND)
		# Check that the user requesting the deletion is the same as the author of the inbox
		if request.user.id == author.user.id:
			inbox = Inbox.objects.filter(author=author)
			inbox.delete()
			return Response(status=status.HTTP_200_OK)
		else:
			return Response(data="User not allowed to delete inbox!", status=status.HTTP_403_FORBIDDEN)