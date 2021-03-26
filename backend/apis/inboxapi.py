from ..models import Author, Comment, Follow, Inbox, Like, Post
from ..serializers import FollowSerializer, LikeSerializer, PostSerializer

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

import socket

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

		if author_id:

			follows_list = Inbox.objects.filter(author=author_id, follow__isnull=False)
			posts_list = Inbox.objects.filter(author=author_id, post__isnull=False)
			likes_list = Inbox.objects.filter(author=author_id, like__isnull=False)

			follows = Follow.objects.filter(follow__in=follows_list)
			posts = Post.objects.filter(post__in=posts_list)
			likes = Like.objects.filter(like__in=likes_list)

			post_serializer = PostSerializer(posts, many=True)
			follow_serializer = FollowSerializer(follows, many=True)
			like_serializer = LikeSerializer(likes, many=True, context={'request': request})

			return Response({
				"type":"inbox",
				"author":"http://"+self.request.META['HTTP_HOST']+"/author/"+author_id,
				"items": follow_serializer.data+like_serializer.data+post_serializer.data
			})
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def create(self, request, author_id=None, *args, **kwargs):

		print("AuthorID: ", author_id, "\n", 'MY Request: ', request.data)

		if author_id:

			if request.data['type'] == 'follow' or request.data['type'] == 'Follow':

				actor_id = request.data['actor']['id'].split("/")[-1]
				object_id = request.data['object']['id'].split("/")[-1]

				actor = Author.objects.filter(id=actor_id).get()
				object = Author.objects.filter(id=object_id).get()

				check_follow = Follow.objects.filter(follower=object, followee=actor)

				if object_id == author_id:
					if check_follow:
						follow = Follow(
							follower=actor,
							followee=object,
							friends = True,
							summary=actor.displayName + " wants to follow " + object.displayName
						)
						check_follow.update(friends=True)

					else:
						follow = Follow(
							follower=actor,
							followee=object,
							summary=actor.displayName + " wants to follow " + object.displayName
						)
					follow.save()
					serializer = self.get_serializer(follow)

					inbox = Inbox(
						author=object,
						follow=follow
					)
					inbox.save()
					return Response(serializer.data, status=status.HTTP_201_CREATED)

			elif request.data['type'] == 'like' or request.data['type'] == 'Like':

				check_id = request.data['object'].split('/')[-1]
				check_type = request.data['object'].split('/')[-2]
				check_author_id = request.data['object'].split('/')[4]
				like_author_id = request.data['author']['id'].split('/')[-1]
				like_author = Author.objects.filter(id=like_author_id).get()
				check_author = Author.objects.filter(id=check_author_id).get()

				if check_author_id == author_id:
					if check_type == 'posts':

						post=Post.objects.filter(id=check_id).get()

						if not Like.objects.filter(author=like_author, post=post):
							like = Like(
								post=post,
								author=like_author,
								summary=like_author.displayName+" Likes your post"
							)
							like.save()
						else:
							return Response(status=status.HTTP_400_BAD_REQUEST)
					if check_type == 'comments':
						post_id = request.data['object'].split('/')[-3]
						comment = Comment.objects.filter(id=check_id)

						if not Like.objects.filter(author=like_author, comment=comment):
							like = Like(
								post=Post.objects.filter(id=post_id).get(),
								author=like_author,
								comment=comment,
								summary=like_author.displayName+" Likes your comment"
							)
							like.save()
						else:
							return Response(status=status.HTTP_400_BAD_REQUEST)
					serializer = LikeSerializer(like, context={'request': request})
					inbox = Inbox(
						author=check_author,
						like=like
					)
					inbox.save()
					return Response(serializer.data, status=status.HTTP_201_CREATED)

			elif request.data['type'] == 'post' or request.data['type'] == 'Post':

				request_author = request.data['author']['id'].split('/')[-1]
				request_post = request.data['id'].split('/')[-1]

				try:
					post_author = Author.objects.filter(id=request_author).get()
				except:
					post_author = Author(
									id = request.data['author']['id'].split('/')[-1],
									user = request.user,
									displayName = request.data['author']['displayName'],
									github = request.data['author']['github'],
									host = request.data['author']['host'],
									url = request.data['author']['url']
									)
					post_author.save()

				try:
					post = Post.objects.filter(id=request_post).get()

				except:

					hostname = socket.gethostbyaddr(request.META.get("HTTP_X_FORWARDED_FOR"))[0]

					if any([types in request.data["contentType"] for types in ['application/base64', 'image/png', 'image/jpeg']]):
						post = Post(
							author = post_author,
							id = request_post,
							title = request.data["title"],
							source = "http://" + hostname + "/author/" + post_author.id + "/posts/" + request_post + "/",
							origin = request.data["origin"],
							description = request.data["description"],
							contentType = request.data["contentType"],
							image_content = request.data["content"],
							categories = request.data["categories"],
							visibility = request.data["visibility"],
							unlisted = request.data["unlisted"]
						)
					else:
						post = Post(
							author = post_author,
							id = request_post,
							title = request.data["title"],
							source = "http://" + hostname + "/author/" + post_author.id + "/posts/" + request_post + "/",
							origin = request.data["origin"],
							description = request.data["description"],
							contentType = request.data["contentType"],
							content = request.data["content"],
							categories = request.data["categories"],
							visibility = request.data["visibility"],
							unlisted = request.data["unlisted"]
						)
					post.save()

				try:
					inbox_author = Author.objects.filter(id=author_id).get()
				except:
					return Response(status=status.HTTP_404_NOT_FOUND)

				inbox = Inbox(
					author=inbox_author,
					post=post
				)
				inbox.save()

				return Response(status=status.HTTP_201_CREATED)
		
			else:
				return Response(data=request, status=status.HTTP_410_GONE)

		else:
			return Response(status=status.HTTP_409_CONFLICT)