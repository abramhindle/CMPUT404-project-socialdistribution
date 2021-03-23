from ..models import Author, Comment, Post
from ..serializers import CommentSerializer

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

class CommentViewSet(viewsets.ModelViewSet):
	"""
	This class specifies the view for the Comment objects. This will run methods to retrieve and edit DB rows and return correctly formatted HTTP responses
	"""

	permission_classes = [
		permissions.AllowAny
	]

	lookup_field = 'post'

	serializer_class = CommentSerializer

	queryset = Comment.objects.all()

	def create(self, request, author_id=None, post_id=None, *args, **kwargs):

		comment = Comment(
			author = Author.objects.filter(id=author_id).get(),
			post = Post.objects.filter(id=post_id).get(),
			comment = request.data["comment"],
			contentType = request.data["contentType"],
			host = self.request.META['HTTP_HOST'],
			post_author_id = author_id
		)
		comment.save()
		serializer = self.get_serializer(comment)
		#serializer = CommentSerializer(data=self.get_serializer(comment).data)
		#serializer.is_valid(raise_exception=True)
		#serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)