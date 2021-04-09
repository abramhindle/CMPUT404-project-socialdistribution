from ..serializers import CommentSerializer
from ..models import Comment, Node
from manager.paginate import ResultsPagination


import json
import requests
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets


class RemoteCommentViewSet(viewsets.ModelViewSet):
	"""
	This class specifies the view for the remote Comment objects. This will run methods to retrieve and edit DB rows and return correctly formatted HTTP responses
	"""

	permission_classes = [
		permissions.AllowAny
	]

	lookup_field = 'post'

	serializer_class = CommentSerializer

	queryset = Comment.objects.all()

	pagination_class = ResultsPagination

	def list(self, request, author_id=None, post_id=None, *args, **kwargs):

		body = json.loads(request.body.decode('utf-8'))
		remote_comments_link = body.get("comments", None)

		
		if request.user.is_authenticated:
			try:
				if remote_comments_link:
					comment_host = remote_comments_link.split('/')[2]
					node = Node.objects.filter(host__icontains=comment_host).get()
					s = requests.Session()
					s.auth = (node.remote_username, node.remote_password)
					s.headers.update({'Content-Type':'application/json'})
					params = {}					
					
					
					if request.query_params.get('page', False):
						params.update({'page': request.query_params.get('page')})
						response_comment = s.get(node.host+"author/"+author_id+"/posts/"+post_id+"/comments", params=params, json=body)
					else:
						response_comment = s.get(node.host+"author/"+author_id+"/posts/"+post_id+"/comments", json=body)
				else:
					raise Exception("The comment link of the remote post is not present!")
			except Exception:
				return Response(data="Unable to get the comments from the remote server!", status=status.HTTP_400_BAD_REQUEST)
			else:
				if response_comment.status_code in [200, 201]:
					return Response(response_comment.json(), status=response_comment.status_code)
				else:
					return Response(data="The remote server encountered an error getting the comments!", status=response_comment.status_code)
