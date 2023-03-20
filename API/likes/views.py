from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..models import AuthorModel, PostsModel, CommentsModel, LikeModel
from ..serializers import PostsSerializer, AuthorSerializer, CommentsSerializer, LikeSerializer
import json
import uuid

@api_view(['POST'])
def InboxView(request, author_id):
    """
    API endpoint that allows users to be viewed or edited.  
    """
    parameters = json.loads(request.body)["object"]
    liker_author_id = parameters["author"].split("/")[3]
    liker_author_object = AuthorModel.objects.get(id=liker_author_id)
    liker_serialized = AuthorSerializer(liker_author_object).data
    liker_author_displayName = liker_serialized["displayName"]
    if "comment" in parameters:
        output = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "summary": liker_author_displayName + " Likes your comment",
        "type": "Like",
        "author": liker_serialized,
        "object": parameters
        }
    else:
        output = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "summary": liker_author_displayName + " Likes your post",
        "type": "Like",
        "author": liker_serialized,
        "object": parameters
        }

    #post_request should be a json object with link to inbox
    LikeModel.objects.create(**output)
    return JsonResponse({"status":"success"}, status = 200)

@api_view(['GET'])
def PostLikeView(request, author_id, post_id):
    """
    for post like function
    """
    post_likes_paginated = []
    object = "http://127.0.0.1:5454/authors/"+ author_id+ "/posts/"+ post_id + "/"
    post_likes_object = LikeModel.objects.filter(object=object)
    for likes in post_likes_object:
        serialized_object = LikeSerializer(likes)
        post_likes_paginated.append(serialized_object.data)
    output = {"object": object, "likes": post_likes_paginated}
    return JsonResponse(output, status = 200)



@api_view(['GET'])
def CommentLikeView(request, author_id, post_id, comment_id):
    """
    for comment like function
    """
    comment_likes_paginated = []
    object = "http://127.0.0.1:5454/authors/"+ author_id+ "/posts/"+ post_id+ "/comments/"+ comment_id + "/"
    comment_likes_object = LikeModel.objects.filter(object=object)
    for likes in comment_likes_object:
        serialized_object = LikeSerializer(likes)
        comment_likes_paginated.append(serialized_object.data)
    output = {"object": object, "likes": comment_likes_paginated}
    return JsonResponse(output, status = 200)