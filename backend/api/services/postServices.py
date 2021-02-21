from ..models import post
from ..serializers import PostSerializer

from rest_framework import status
from rest_framework.response import Response
from django.core import serializers
import json, sys

class postServices():
  @staticmethod
  def creatNewPost(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
      postInstance = serializer.save()
      # set url for created post model
      postInstance.url = request.build_absolute_uri() + str(postInstance.post_id)
      postInstance.save()
      return Response(status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)

  @staticmethod
  def getPostById(request, post_id, author_id=None):
    data = post.Post.objects.all()
    # try to filter for such post
    try:
      data = data.filter(post_id__exact=post_id)
      data = serializers.serialize('json', data)
      data = json.loads(data)[0]['fields']
      data['post_id'] = post_id
    # return 404 if such post does not exist
    except:
      return Response(status=status.HTTP_404_NOT_FOUND)

    # verify author id, if author id not match return 404
    if author_id and data['author_id'] == author_id:
      return Response(data)
    else:
      return Response(status=status.HTTP_404_NOT_FOUND)
