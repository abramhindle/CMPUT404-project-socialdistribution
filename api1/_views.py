from rest_framework.decorators import api_view
from django.http import JsonResponse
from social_net.api.models import AuthorModel, PostsModel, CommentsModel, LikeModel, FollowModel
from social_net.api.serializers import PostsSerializer, AuthorSerializer, CommentsSerializer, LikeSerializer
import json
import uuid

@api_view(['GET', 'POST'])
def AuthorView(request, uid):
    """
    API endpoint that allows users to be viewed or edited.
    """
    if request.method == 'GET':
        try:
            author_object = AuthorModel.objects.get(id=uid)
        except AuthorModel.DoesNotExist:
            return JsonResponse({"Error": "Author does not exist"}, status = 404)

        serialized_object = AuthorSerializer(author_object)

        output = serialized_object.data
        return JsonResponse(output, status = 200)
    elif request.method == 'POST':
        parameters = json.loads(request.body)
        AuthorModel.objects.filter(id=uid).update(**parameters)
        return JsonResponse({
            "success": True,
        },status = 200)
   
@api_view(['GET', 'POST'])
def AuthorsView(request):
    """
    API endpoint that allows authors to be viewed or created.
    """
    if request.method == 'GET':
        page = int(request.GET.get('page', '1'))
        size = int(request.GET.get('size', '5'))
        query = request.GET.get('query')
        authors_list = AuthorModel.objects.filter(displayName__icontains=query).order_by('-displayName')[page*size-5:page*size-1]
        serialized_authors_list = list([AuthorSerializer(author).data for author in authors_list])
        serialized_authors_list = list([AuthorSerializer(author).data for author in authors_list])
        output = {
        "type": "authors",      
        "items": serialized_authors_list,
        }
        return JsonResponse(output, status = 200)

    ## More for internal use
    elif request.method == 'POST':
        parameters = json.loads(request.body)
        AuthorModel.objects.create(
            **parameters
        )
        
        return JsonResponse({
            "success": True,
        },status = 200)
   

@api_view(['GET'])
def AuthorFollowersView(request, uid):
    """
    API endpoint that gets all the followes of an author
    """
    
    followers_ids = FollowModel.objects.all().filter(followers=uid, status="accepted")

    followers = []
    for follower in followers_ids:
        followers.append(follower.follower)

    author_object = AuthorModel.objects.all().filter(id__in=followers)

    serialized_object = AuthorSerializer(author_object, many=True)
    return JsonResponse({
        "type": "followers",
        "items": serialized_object.data,
    }, status = 200)

@api_view(['DELETE', 'PUT', 'GET'])
def AuthorFollowersOperationsView(request, uid, foreign_uid):
    """
    API endpoint that allows aurthors to be followed or unfollowed
    """

    if request.method == 'GET':
        is_follower = FollowModel.objects.filter(follower=uid, following=foreign_uid).exists()
        if is_follower:
            return JsonResponse({"status": True}, status = 200)
        else:
            return JsonResponse({"status": False}, status = 200)

    elif request.method == 'PUT':
        FollowModel.objects.create(
            follower=uid,
            following=foreign_uid,
            status="accepted"
        )
        return JsonResponse({"status": "success"}, status = 200)
    
    elif request.method == 'DELETE':
        FollowModel.objects.filter(follower=uid, following=foreign_uid).delete()
        return JsonResponse({"status": "success"}, status = 200)

    

@api_view(['GET', 'POST'])
def PostsView(request, author_id:str):
    """
    API endpoint that allows users to be viewed or edited.
    """
   
    posts_paginated = []
    if request.method == 'GET':
        page = int(request.GET.get('page', '0'))
        count = int(request.GET.get('count', '10'))
        count = max(count, 25)
        post_object = PostsModel.objects.filter(author=author_id).order_by('-published')[page*count:page*count+count]
        for post in post_object:
            serialized_object = PostsSerializer(post)
            author_data = AuthorModel.objects.get(id=post.author)
            comment_data = CommentsModel.objects.all().filter(post_id=post.id)
            
            serialized_author = AuthorSerializer(author_data)
            serialized_comments = CommentsSerializer(comment_data, many=True)
            data = dict(serialized_object.data)
            data['author'] = serialized_author.data
            data['comments'] = serialized_comments
            data['commentSrc'] = {
                "type": "comments",
                "page": 1,
                "size": 5,
                "post": post.id,
                "id": comment_data.id,
                "comments": serialized_comments
            }
            posts_paginated.append(data)
        
        ## sort by published
        posts_paginated = sorted(posts_paginated, key=lambda k: k['published'], reverse=True)

        return JsonResponse(posts_paginated, status = 200)
    elif request.method == 'POST':
        json_data = json.loads(request.body)
        PostsModel.objects.create(author=author_id, id=str(uuid.uuid4()), **json_data)
        return JsonResponse({"status":"success"}, status = 200)

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def PostsRetrieveView(request, author_id, post_id):
    """
    API endpoint that allows users to be viewed or edited.
    """
    if request.method == 'GET':
        post_object = PostsModel.objects.get(id=post_id)
        author_data = AuthorModel.objects.get(id=post_object.author)
        serialized_author = AuthorSerializer(author_data)
        serialized_object = PostsSerializer(post_object)
        data = dict(serialized_object.data)
        data['author'] = serialized_author.data
        return JsonResponse(data, status = 200)
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
        json_data = json.loads(request.body)
        PostsModel.objects.filter(author=author_id, id=post_id).update(**json_data)
        return JsonResponse({"status":"success"}, status = 200)

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



@api_view(['POST', 'GET'])
def InboxView(request, author_id):
    """
    API endpoint that allows users to be viewed or edited.
    """
    if request.method == 'POST':

        parameters = json.loads(request.body)

        liker_author_id = parameters["author"].split("/")[3]
        liker_author_object = AuthorModel.objects.get(id=liker_author_id)
        liker_serialized = AuthorSerializer(liker_author_object).data
        liker_author_displayName = liker_serialized["displayName"]
        if parameters["type"] == "comment":
            output = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": liker_author_displayName + " Likes your comment",
            "type": "Like",
            "author": liker_serialized,
            "object": parameters
            }
        elif parameters["type"] == "Like":
            output = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": liker_author_displayName + " Likes your post",
            "type": "Like",
            "author": liker_serialized,
            "object": parameters
            }
        elif parameters["type"] == "post":
            output = {
                "type": "post",
                "title": parameters["title"],
                "source": parameters["source"],
                "origin": parameters["origin"],
                "description": parameters["description"],
                "contentType": parameters["contentType"],
                "content": parameters["content"],
                "author": parameters["author"],
                "categories": parameters["categories"],
                "count": parameters["count"],
                "size": parameters["size"],
                "comments": parameters["comments"],
                "published": parameters["published"],
                "visibility": parameters["visibility"],
                "unlisted": parameters["unlisted"],
            }
        elif parameters["type"] == "Follow":
            output = {
                "type": "Follow",
                "summary": liker_author_displayName + " Followed you",
                "actor": liker_serialized,
                "object": parameters["object"]
            }
        
    #post_request should be a json object with link to inbox
    LikeModel.objects.create(**output)
    return JsonResponse({"status":"success"}, status = 200)

@api_view(['GET'])
def PostLikeView(request, author_id, post_id):
    """
    API endpoint that allows users to be viewed or edited.
    """
    post_likes_paginated = []
    object = "http://127.0.0.1:5454/authors/"+ author_id+ "/posts/"+ post_id
    post_likes_object = LikeModel.objects.filter(object=object)
    for likes in post_likes_object:
        serialized_object = LikeSerializer(likes)
        post_likes_paginated.append(serialized_object.data)
    output = {"object": object, "likes": post_likes_paginated}
    return JsonResponse(output, status = 200)



@api_view(['GET'])
def CommentLikeView(request, author_id, post_id, comment_id):
    """
    API endpoint that allows users to be viewed or edited.
    """
    comment_likes_paginated = []
    object = "http://127.0.0.1:5454/authors/"+ author_id+ "/posts/"+ post_id+ "/comments/"+ comment_id + "/"
    comment_likes_object = LikeModel.objects.filter(object=object)
    for likes in comment_likes_object:
        serialized_object = LikeSerializer(likes)
        comment_likes_paginated.append(serialized_object.data)
    output = {"object": object, "likes": comment_likes_paginated}
    return JsonResponse(output, status = 200)

@api_view(['GET'])
def LikedView(request, author_id):
    """
    API endpoint that allows users to be viewed or edited.
    """
    liked_paginated = []
    liked_object = LikeModel.objects.filter(author=author_id)
    for liked in liked_object:
        serialized_object = LikeSerializer(liked)
        if "comments" not in serialized_object["object"]:
            post_id = liked["object"].split("/")[6]
            post_object = PostsSerializer(PostsModel.objects.get(id=post_id)).data["visibility"]
            if post_object == "PUBLIC":
                liked_paginated.append(serialized_object.data)
    output = {"author_id": author_id, "likes": liked_paginated}
    return JsonResponse(output, status = 200)
