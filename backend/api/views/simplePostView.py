from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core import serializers

from ..models import post
from ..serializers import PostSerializer

import json, sys
#########################################
# post request, asking for 
#    title, str
#    author_id, uuid
#    description, str
#    content, str
#    visibility, str
#
# return: None
##########################################
@api_view(['POST'])
def createPost(request, author_id):
  request.data['author_id'] = author_id
  serializer = PostSerializer(data=request.data)
  if serializer.is_valid():
    postInstance = serializer.save()
    # set url for created post model
    postInstance.url = request.build_absolute_uri() + str(postInstance.post_id)
    postInstance.save()
    return Response(status=status.HTTP_201_CREATED)

  return Response(status=status.HTTP_400_BAD_REQUEST)

############################################
# get request
#
# args: author_id and post_id
#
# return query result in json list
################################################
@api_view(['GET'])
def getPost(request, author_id, post_id):
  data = post.Post.objects.all()
  # try to filter for such post
  try:
    data = data.filter(post_id__exact=post_id, author_id__exact=author_id)
    data = serializers.serialize('json', data)
    data = json.loads(data)[0]['fields']
    data['post_id'] = post_id
  # return 404 if such post does not exist
  except:
    return Response(status=status.HTTP_404_NOT_FOUND)

  return Response(data)

############################################
# post request
#
# args: author_id and post_id
#
# return updated post data
################################################
@api_view(['POST'])
def editPost(request, author_id, post_id):
  data = post.Post.objects.get(pk=post_id)

  body = request.body.decode('utf-8')
  body = json.loads(body)
  try:
    for key_of_update in body:
      value_of_update = body.get(key_of_update, None)

      setattr(data, key_of_update, value_of_update)
    data.save()
    return Response(status=status.HTTP_200_OK)

  except:
    return Response(status=status.HTTP_400_BAD_REQUEST)


############################################
# handle request for url author/<str:author_id>/posts/<str:post_id>
#
# args: author_id and post_id
#
# GET request: getPost
# POST request: editPost
################################################
def handlePostRequest(request, author_id, post_id):
  if request.method == "GET":
    return getPost(request, author_id, post_id)
  elif request.method == "POST":
    return editPost(request, author_id, post_id)