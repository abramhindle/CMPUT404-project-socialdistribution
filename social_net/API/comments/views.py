from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..models import AuthorModel, PostsModel, CommentsModel, LikeModel
from ..serializers import PostsSerializer, AuthorSerializer, CommentsSerializer, LikeSerializer
import json
import uuid

@api_view(['GET', 'POST'])
def CommentsView(request, author_id, post_id):
    """
    API endpoint that allows users to be viewed or edited.
    """
    posts_paginated = []
    page = int(request.GET.get('page', '1'))
    size = int(request.GET.get('size', '5'))
    if request.method == 'GET':
        post_object = CommentsModel.objects.filter(post_id=post_id).order_by('-published')[page*size-5:page*size-1]
        for post in post_object:
            serialized_object = CommentsSerializer(post)
            serialized_object.data["author"] = AuthorSerializer(AuthorModel.objects.get(id=serialized_object.data["author"])).data
            posts_paginated.append(serialized_object.data)
        output = {"type":"comments",
            "page": page,
            "size": size,
            "post": post_id,
            "id": post_id, #TODO: i have no idea what is going on here?
            "comments": posts_paginated}
        return JsonResponse(output, status = 200)
    elif request.method == 'POST':
        parameters = json.loads(request.body)
        if parameters["type"] == "comment":
            CommentsModel.objects.create(**parameters)
        post_object = CommentsModel.objects.filter(post_id=post_id).order_by('-published')[page*size-5:page*size-1]
        for post in post_object:
            serialized_object = CommentsSerializer(post)
            serialized_object.data["author"] = AuthorSerializer(AuthorModel.objects.get(id=serialized_object.data["author"])).data
            posts_paginated.append(serialized_object.data)
        output = {"type":"comments",
            "page": page,
            "size": size,
            "post": post_id,
            "id": post_id, #TODO: i have no idea what is going on here?
            "comments": posts_paginated}
        return JsonResponse(output, status = 200)
