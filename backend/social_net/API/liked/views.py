from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..models import AuthorModel, PostsModel, CommentsModel, LikeModel
from ..serializers import PostsSerializer, AuthorSerializer, CommentsSerializer, LikeSerializer
import json
import uuid

@api_view(['GET'])
def LikedView(request, author_id):
    """
    API endpoint that allows users to be viewed or edited.
    """
    liked_paginated = []
    liked_object = LikeModel.objects.filter(author=author_id)
    for liked in liked_object:
        serialized_object = LikeSerializer(liked).data
        if "comments" not in serialized_object["object"]:
            post_id = liked["object"].split("/")[6]
            post_object = PostsSerializer(PostsModel.objects.get(id=post_id)).data["visibility"]
            if post_object == "PUBLIC":
                liked_paginated.append(serialized_object.data)
    output = {"author_id": author_id, "likes": liked_paginated}
    return JsonResponse(output, status = 200)
