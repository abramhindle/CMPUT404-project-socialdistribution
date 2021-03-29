from manager.settings import HOSTNAME
from manager.paginate import ResultsPagination
from ..models import Author, Comment, Follow, Inbox, Like, Post, Node
from ..serializers import CommentSerializer, FollowSerializer, LikeSerializer, PostSerializer

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

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

			# Retrieve the author ID's for the actor and object

			actor_id = body['actor']['id'].split("/")[-1]
			object_id = body['object']['id'].split("/")[-1]

			if actor_id == "" or object_id == "":
				return Response(data="Invalid author ID passed", status=status.HTTP_400_BAD_REQUEST)

			# Check if author ID is matching
			if object_id != author.id:
				return Response(data="Author doesn't match request followee", status=status.HTTP_400_BAD_REQUEST)
			# Check if the object exists in the database
			try:
				actor = Author.objects.filter(id=actor_id).get()
			except:
				actor = Author(
					id = actor_id,
					user = request.user,
					displayName = body["actor"]["displayName"],
					github = body["actor"]["github"],
					host = body["actor"]["host"],
					url = body["actor"]["url"]
				)
				actor.save()

			# Check if this follow already exists
			try:
				alreadyFollow = Follow.objects.filter(follower=actor, followee=author).get()
				return Response(data="Follow already exists"+str(actor_id)+str(object_id), status=status.HTTP_409_CONFLICT)
			except:
				pass

			# Check if the authors are already following each other
			check_follow = Follow.objects.filter(follower=author, followee=actor)
			# If the actor is already followed by the object
			if check_follow:
				follow = Follow(
					follower=actor,
					followee=author,
					friends = True,
					summary=actor.displayName + " wants to follow " + author.displayName
				)
				check_follow.update(friends=True)
			# If the authors are not currently following each other
			else:
				follow = Follow(
					follower=actor,
					followee=author,
					summary=actor.displayName + " wants to follow " + author.displayName
				)
			follow.save()
			serializer = self.get_serializer(follow)
			# Add this follow to the inbox of the author ID provided
			inbox = Inbox(
				author=author,
				follow=follow
			)
			inbox.save()
			# Return the follow object
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		# If the sent object is of type Like
		elif body['type'].lower() == 'like':

			# Parse the input object and author ID
			object_data = body['object'].split('/')
			like_author_data = body['author']['id'].split('/')

			comment = None
			post = None

			# Check the length of the object URL, 9 is for Comment likes
			if len(object_data) == 9 or len(object_data) == 10:
				try:
					# Get the comment and post associated
					comment = Comment.objects.filter(id=object_data[-1]).get()
					post = Post.objects.filter(id=object_data[-3]).get()
				except:
					return Response(data="Comment does not exist", status=status.HTTP_404_NOT_FOUND)
			# A length of 7 is for Post likes
			elif len(object_data) == 7 or len(object_data) == 8:
				try:
					# Get the post associated
					post = Post.objects.filter(id=object_data[-1]).get()
				except:
					return Response(data="Post does not exist", status=status.HTTP_404_NOT_FOUND)
			else:
				return Response(data="Object being liked not found", status=status.HTTP_404_NOT_FOUND)

			# Check if the request URL ID is for the post or comment creator
			if post.author.id == author_id or comment.author.id == author_id:

				# Retrieve the author of the Like or create an author if they are remote
				try:
					like_author = Author.objects.filter(id=like_author_data[-1]).get()
				except:
					if like_author_data[-1] != "":
						like_author = Author(
							id = like_author_data[-1],
							user = request.user,
							displayName = body["actor"]["displayName"],
							github = body["actor"]["github"],
							host = body["actor"]["host"],
							url = body["actor"]["url"]
							)
						like_author.save()
					else:
						return Response(data="Like author ID not valid", status=status.HTTP_400_BAD_REQUEST)

				# If the Like is on a Comment
				if comment is not None:
					# Check if the Like already exists in the database for the Comment
					if not Like.objects.filter(author=like_author, comment=comment):
						try:
							like = Like(
								post=post,
								author=like_author,
								comment=comment,
								summary=like_author.displayName+" Likes your comment"
							)
							inbox = Inbox(
								author=comment.author,
								like=like
							)
							like.save()
							inbox.save()
						except Exception as e:
							return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
					else:
						return Response(data="Like already exists for this comment", status=status.HTTP_409_CONFLICT)

				# If the Like is on a Post
				elif post is not None:
					# Check if the Like already exists in the database for the Post
					if not Like.objects.filter(author=like_author, post=post):
						try:
							like = Like(
								post=post,
								author=like_author,
								summary=like_author.displayName+" Likes your post"
							)
							inbox = Inbox(
								author=post.author,
								like=like
							)
							like.save()
							inbox.save()
						except Exception as e:
							return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
					else:
						return Response(data="Like already exists for this post", status=status.HTTP_409_CONFLICT)


				serializer = LikeSerializer(like, context={'request': request})
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		# If the sent object is of type Post
		elif body['type'].lower() == 'post':
			# Parse request for author of the post and post ID
			request_author_id = body['author']['id'].split('/')[-1]
			request_post_id = body['id'].split('/')[-1]
			# Check if the ID is blank
			if request_author_id == "":
				request_author_id = body['author']['id'].split('/')[-2]
			# Check if the ID is blank
			if request_post_id == "":
				request_post_id = body['id'].split('/')[-2]
			# Check if the author exists in the database, otherwise add the author
			try:
				post_author = Author.objects.filter(id=request_author_id).get()
			except:
				post_author = Author(
								id = request_author_id,
								user = request.user,
								displayName = body['author']['displayName'],
								github = body['author']['github'],
								host = body['author']['host'],
								url = body['author']['url'],
								)
				post_author.save()
			# Check if the post exists in the database
			try:
				post = Post.objects.filter(id=request_post_id).get()
			# Otherwise create the post locally for distribution
			except:
				# Check the contentType for images
				try:
					if any([types in request.data["contentType"] for types in ['application/base64', 'image/png', 'image/jpeg']]):
						post = Post(
							author = post_author,
							id = request_post_id,
							title = body["title"],
							source = body["source"],
							origin = body["origin"],
							description = body["description"],
							contentType = body["contentType"],
							image_content = body["content"],
							categories = body["categories"],
							visibility = body["visibility"],
							unlisted = body["unlisted"]
						)
					# If the contentType is not for images
					else:
						post = Post(
							author = post_author,
							id = request_post_id,
							title = body["title"],
							source = body["source"],
							origin = body["origin"],
							description = body["description"],
							contentType = body["contentType"],
							content = body["content"],
							categories = body["categories"],
							visibility = body["visibility"],
							unlisted = body["unlisted"]
						)
					post.save()
				except Exception as e:
					return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
			# Check if the inbox owner is a valid author
			try:
				inbox_author = Author.objects.filter(id=author_id).get()
			except:
				return Response(status=status.HTTP_404_NOT_FOUND)
			# Add the post to the inbox
			try:
				inbox = Inbox(
					author=inbox_author,
					post=post
				)
				inbox.save()
			except Exception as e:
					return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)

			return Response(status=status.HTTP_201_CREATED)

		# If the sent object is of type Comment
		elif request.data['type'].lower() == 'comment':

			# Parse the author and id of the body to find the comment id, the author of the comment, and the post id that the comment is on
			request_author_id = request.data['author']['id'].split('/')[-1]
			request_comment_id = body['id'].split('/')[-1]
			request_post_id = body['id'].split('/')[-3]

			# Check if any of the previous values is blank, and try to locate it elsewhere
			if request_author_id == "":
				request_author_id = body['author']['id'].split('/')[-2]

			if request_comment_id == "":
				request_comment_id = body['id'].split('/')[-2]

			if request_post_id == "comments":
				request_comment_id = body['id'].split('/')[-4]

			# Get the author of the comment, if they do not exists create a local author object for them to associate to the comment
			try:
				comment_author = Author.objects.filter(author=request_author_id).get()
			except:
				try:
					comment_author = Author(
									id = request_author_id,
									user = request.user,
									displayName = request.data['author']['displayName'],
									github = request.data['author']['github'],
									host = request.data['author']['host'],
									url = request.data['author']['url'],
									)
					comment_author.save()
				except Exception as e:
					return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
			# Check that the post being commented on exists
			try:
				post = Post.objects.filter(id=request_post_id).get()
			except:
				return Response(status=status.HTTP_404_NOT_FOUND, data="Could not find the post the comment belongs to!")
			# Check if the comment already exists, if it does not add the comment to the database
			try:
				received_comment = Comment.objects.filter(id=request_comment_id).get()
			except:
				# Create th comment object in the database
				try:
					request_host = request.data['id'].split('/')[2]
					received_comment = Comment(
						id = request_comment_id,
						author = comment_author,
						post = post,
						comment = request.data.get('comment', None),
						contentType = request.data.get('contentType', None),
						host = request_host,
						post_author = post.author.id,
					)
					received_comment.save()
				except Exception as e:
					return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

			# Try to get the author whos inbox the comment needs to be added to and return a 404 if they are not found
			try:
				inbox_author = Author.objects.filter(id=author_id).get()
			except:
				return Response(status=status.HTTP_404_NOT_FOUND)

			# Add the post to the inbox
			try:
				inbox = Inbox(
					author=inbox_author,
					icomment=received_comment
				)
				inbox.save()
			except Exception as e:
					return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response(data=request, status=status.HTTP_410_GONE)

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