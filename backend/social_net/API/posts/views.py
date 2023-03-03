from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..models import AuthorModel, PostsModel, CommentsModel, LikeModel
from ..serializers import PostsSerializer, AuthorSerializer, CommentsSerializer, LikeSerializer
import json
import uuid

@api_view(['GET', 'POST'])
def PostsView(request, author_id):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #checks friendship
    posts_paginated = []
    if request.method == 'GET':
        post_object = PostsModel.objects.filter(author=author_id).order_by('-published')[0:4] #TODO: pagination
        for post in post_object:
            serialized_object = PostsSerializer(post)
            posts_paginated.append(serialized_object.data)
        output = {"posts": posts_paginated}
        return JsonResponse(output, status = 200)
    elif request.method == 'POST':
        pid=str(uuid.uuid4())
        PostsModel.objects.create(author=author_id, id=pid)
        return JsonResponse({"status":"success","id":pid}, status = 200)

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def PostsRetriveView(request, author_id, post_id):
    """
    API endpoint that allows users to be viewed or edited.
    """
    if request.method == 'GET':
        post_object = PostsModel.objects.get(id=post_id)
        serialized_object = PostsSerializer(post_object)
        return JsonResponse(serialized_object.data, status = 200)
    elif request.method == 'POST':
        post_object = PostsModel.objects.get(id=post_id)
        serialized_object = PostsSerializer(post_object)
        parameters = json.loads(request.body)
        serialized_object.update(post_object, parameters)
        return JsonResponse({"status":"success"}, status = 200)
    elif request.method == 'DELETE':
        PostsModel.objects.filter(author=author_id, id=post_id).delete()
        return JsonResponse({"status":"success"}, status = 200)
    elif request.method == 'PUT':
        PostsModel.objects.create(author=author_id, id=post_id)
        return JsonResponse({"status":"success"}, status = 200)
