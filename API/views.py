from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from django.http import JsonResponse
from .models import AuthorModel, PostsModel, CommentsModel, LikeModel
from .serializers import PostsSerializer, AuthorSerializer, CommentsSerializer, LikeSerializer
import json
import uuid


class PermittedForRemote(BasePermission):
    """
    Custom permission class that determines permissions based on the endpoint
    the request is accessing.
    
    This is intended to be used in a decorator like this:
        @permission_classes([IsAdminUser|IsAuthenticated&PermittedForRemote])
    
    When used in such a decorator, it's like a janky way of saying, "you can
    only use this endpoint's method if you're either an admin or an an
    authenticated remote node. In the latter case, you can only access a subset
    of the endpoint's methods."
    This allows us to just set our frontend as an admin user so it can access
    all the endpoints it needs to, while restricting other nodes (authenticated
    non-admins) to endpoint methods marked 'remote' in the spec. This is
    probably a terrible way of accomplishing this. Feel free to make better
    (perhaps an API token would be a better solution for the frontend.)
    """
    
    remote_views = {'GET': ['AuthorsView', 'AuthorView', 'AuthorFollowersView',
                            'AuthorFollowersOperationsView', 'PostsView',
                            'PostsRetrieveView', 'CommentsView', 'PostLikeView',     # TODO: Add ImagePostView once it exists
                            'CommentLikeView', 'LikedView', 'FollowView'],      # NOTE: FollowView may or may not be the same thing as AuthorFollowersOperationsView, except AuthorFollowersOperationsView seems to have a bug in urls.py.
                    'POST': ['InboxView']}      # XXX: There's some funky stuff in the spec for POSTing to the inbox and likes endpoint. May cause problems later. See: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#inbox and https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#likes
    def has_permission(self, request, view):
        name = view.__class__.__name__
        return name in self.remote_views[request.method]


# FIXME: According to the spec, it should be POST, not PUT: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#single-author
@api_view(['GET', 'PUT'])
@permission_classes([IsAdminUser|IsAuthenticated&PermittedForRemote])
def AuthorView(request, uid):
    """
    API endpoint that allows users to be viewed or edited.
    
    URL: ://service/authors/{AUTHOR_ID}/
        GET [local, remote]: retrieve AUTHOR_ID’s profile
        POST [local]: update AUTHOR_ID’s profile
        
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#single-author
    """
    
    if request.method == 'GET':
        try:
            author_object = AuthorModel.objects.get(id=uid)
        except AuthorModel.DoesNotExist:
            return JsonResponse({"Error": "Author does not exist"}, status = 404)

        serialized_object = AuthorSerializer(author_object)

        output = serialized_object.data
        return JsonResponse(output, status = 200)
    # FIXME: According to the spec, it should be POST, not PUT: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#single-author
    elif request.method == 'PUT':
        parameters = json.loads(request.body)
        AuthorModel.objects.filter(id=uid).update(**parameters)
        
        return JsonResponse({"success":True,}, status = 200)


# FIXME: According to the spec, this should only support GET, and not POST: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#authors
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser|IsAuthenticated&PermittedForRemote])
def AuthorsView(request):
    """
    API endpoint for getting all authors on the server
    
    URL: ://service/authors/
        GET [local, remote]: retrieve all profiles on the server (paginated)
            page: how many pages
            size: how big is a page
    Example query: GET ://service/authors?page=10&size=5
        Gets the 5 authors, authors 45 to 49.
        
    See Also:
    https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#authors
    """
    
    if request.method == 'GET':
        page = int(request.GET.get('page', '1'))
        size = int(request.GET.get('size', '5'))
        authors_list = AuthorModel.objects.order_by('-displayName')[page*size-5:page*size-1]
        serialized_authors_list = list([AuthorSerializer(author).data for author in authors_list])
        output = {
        "type": "authors",      
        "items": serialized_authors_list,
        }
        return JsonResponse(output, status = 200)

    elif request.method == 'POST':
        parameters = json.loads(request.body)
        AuthorModel.objects.create(**parameters)

        return JsonResponse({"success":True,}, status = 200)
   

@api_view(['GET'])
@permission_classes([IsAdminUser|IsAuthenticated&PermittedForRemote])
def AuthorFollowersView(request, uid):
    """
    API endpoint to get a list of an author's followers.
    
    URL: ://service/authors/{AUTHOR_ID}/followers
        GET [local, remote]: get a list of authors who are AUTHOR_ID’s followers
                
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#followers
    """
    
    author_object = AuthorModel.objects.get(id=uid).followers
    # serialized_object = AuthorSerializer(author_object)
    # output = serialized_object.data
    return JsonResponse({uid:author_object}, status = 200)


@api_view(['DELETE', 'PUT', 'GET'])
@permission_classes([IsAdminUser|IsAuthenticated&PermittedForRemote])
def AuthorFollowersOperationsView(request, uid, foreign_uid):
    """
    API endpoint doing things with an author's followers.
    
    URL: ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
        DELETE [local]: remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
        PUT [local]: Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)
        GET [local, remote] check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
        
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#followers
    """

    if request.method == 'GET':
        author_object = AuthorModel.objects.get(id=uid).followers
        if foreign_uid in author_object:
            return JsonResponse({"status": "success"}, status = 200)
        else:
            return JsonResponse({"status": "failure"}, status = 200)

    elif request.method == 'PUT':
        author_object = AuthorModel.objects.get(id=uid)
        author_object.followers.append(foreign_uid)
        serialized_object = AuthorSerializer(author_object)
        parameters = json.loads(request.body)
        output = serialized_object.data
        author_object.save()
        return JsonResponse(output, status = 200)
    
    elif request.method == 'DELETE':
        author_object = AuthorModel.objects.get(id=uid)
        author_object.followers.remove(foreign_uid)
        serialized_object = AuthorSerializer(author_object)
        parameters = json.loads(request.body)
        output = serialized_object.data
        author_object.save()
        return JsonResponse(output, status = 200)
    

# XXX Please Check: I think this is supposed to just go to the inbox and let the
# inbox handle the GETing and POSTing and such.
# See: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#friendfollow-request
# And: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#inbox
# NOTE: Currently this is set to the same url as AuthorFollowersOperationsView,
# except that view also has a bug in the urls.py (missing a / between a
# directory and a follower_id)
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser|IsAuthenticated&PermittedForRemote])
def FollowView(request, author_uid, foreign_uid):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #checks friendship
    if request.method == 'GET':
        print("author_uid: ", author_uid)
        print("foreign_uid: ", foreign_uid)
        author_object_followers = AuthorModel.objects.get(id=author_uid).followers
        foreign_object_followers = AuthorModel.objects.get(id=foreign_uid).followers
        if foreign_uid in author_object_followers and author_uid in foreign_object_followers:
            return JsonResponse({"status": "FRIENDS"}, status = 200)
        elif foreign_uid in author_object_followers:
            return JsonResponse({"status": "FOLLOWED_BY"}, status = 200)
        elif author_uid in foreign_object_followers:
            return JsonResponse({"status": "FOLLOWING"}, status = 200)
        else:
            return JsonResponse({"status": "NOT_FRIENDS"}, status = 200)
        
    elif request.method == 'POST':
        author_object = AuthorModel.objects.get(id=author_uid)
        foreign_object = AuthorModel.objects.get(id=foreign_uid)
        ## check if already friends
        if author_object.id in foreign_object.followers:
            author_object.following.remove(foreign_uid)
            foreign_object.followers.remove(author_uid)
            ## make a set to remove duplicates
            author_object.following = list(set(author_object.following))
            foreign_object.followers = list(set(foreign_object.followers))
            author_object.save()
            foreign_object.save()
            return JsonResponse({"status": "success"}, status = 200)

        author_object.following.append(foreign_uid)
        foreign_object.followers.append(author_uid)
        ## make a set to remove duplicates
        author_object.following = list(set(author_object.following))
        foreign_object.followers = list(set(foreign_object.followers))
        author_object.save()
        foreign_object.save()
        return JsonResponse({"status": "success"}, status = 200)


@api_view(['GET'])
@permission_classes([IsAdminUser|IsAuthenticated&PermittedForRemote])
def SearchView(request):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #checks friendship
    if request.method == 'GET':
        query = request.GET.get('query')
        authors_list = AuthorModel.objects.filter(displayName__icontains=query)
        serialized_authors_list = list([AuthorSerializer(author).data for author in authors_list])
        output = {
        "type": "authors",      
        "items": serialized_authors_list,
        }
        return JsonResponse(output, status = 200)


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser|IsAuthenticated&PermittedForRemote])
def PostsView(request, author_id):
    """
    API endpoint for getting multiple posts drom an author (or making a new post
    with random id).
    
    Creation URL ://service/authors/{AUTHOR_ID}/posts/
        GET [local, remote] get the recent posts from author AUTHOR_ID (paginated)
        POST [local] create a new post but generate a new id
    Be aware that Posts can be images that need base64 decoding.
        posts can also hyperlink to images that are public
        
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#post
    """
    #checks friendship
    posts_paginated = []
    if request.method == 'GET':
        page = int(request.GET.get('page', '0'))
        count = int(request.GET.get('count', '10'))
        following = request.GET.get('following')
        count = max(count, 25)
        post_object = PostsModel.objects.filter(author=author_id).order_by('-published')[page*count:page*count+count]
        for post in post_object:
            serialized_object = PostsSerializer(post)
            author_data = AuthorModel.objects.get(id=post.author)
            serialized_author = AuthorSerializer(author_data)
            data = dict(serialized_object.data)
            data['author'] = serialized_author.data
            posts_paginated.append(data)

        if following:
            author_object = AuthorModel.objects.get(id=author_id)
            for follower in author_object.following:
                follower_posts = PostsModel.objects.filter(author=follower).order_by('-published')[page*count:page*count+count]
                for post in follower_posts:
                    serialized_object = PostsSerializer(post)
                    author_data = AuthorModel.objects.get(id=post.author)
                    serialized_author = AuthorSerializer(author_data)
                    data = dict(serialized_object.data)
                    data['author'] = serialized_author.data
                    if data['unlisted'] == False:
                        posts_paginated.append(data)

        ## sort by published
        posts_paginated = sorted(posts_paginated, key=lambda k: k['published'], reverse=True)
        output = {"posts": posts_paginated}

        return JsonResponse(output, status = 200)
    elif request.method == 'POST':
        json_data = json.loads(request.body)
        PostsModel.objects.create(author=author_id, id=str(uuid.uuid4()), **json_data)
        return JsonResponse({"status":"success"}, status = 200)


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAdminUser|IsAuthenticated&PermittedForRemote])
def PostsRetrieveView(request, author_id, post_id):
    """
    API endpoint for CRUD operations on a post with specified id.
    
    URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}
        GET [local, remote] get the public post whose id is POST_ID
        POST [local] update the post whose id is POST_ID (must be authenticated)
        DELETE [local] remove the post whose id is POST_ID
        PUT [local] create a post where its id is POST_ID
    Be aware that Posts can be images that need base64 decoding.
        posts can also hyperlink to images that are public
        
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#post
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


# TODO: IMAGE POST ENDPOINT: URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/image
# https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#image-posts


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser|IsAuthenticated&PermittedForRemote])
def CommentsView(request, author_id, post_id):
    """
    API endpoint getting and making comments on an author's post.
    
    URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
        GET [local, remote] get the list of comments of the post whose id is POST_ID (paginated)
        POST [local] if you post an object of “type”:”comment”, it will add your comment to the post whose id is POST_ID
        
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#comments
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



@api_view(['POST'])
@permission_classes([IsAdminUser|IsAuthenticated&PermittedForRemote])
def InboxView(request, author_id):
    """
    API endpoint for sending and retrieving new content for authors across nodes.
    One of the only endpoints that allows POSTs to remote nodes.
    
    The inbox is all the new posts from who you follow
    URL: ://service/authors/{AUTHOR_ID}/inbox
        GET [local]: if authenticated get a list of posts sent to AUTHOR_ID (paginated)
        POST [local, remote]: send a post to the author
            if the type is “post” then add that post to AUTHOR_ID’s inbox
            if the type is “follow” then add that follow is added to AUTHOR_ID’s inbox to approve later
            if the type is “like” then add that like to AUTHOR_ID’s inbox
            if the type is “comment” then add that comment to AUTHOR_ID’s inbox
        DELETE [local]: clear the inbox
        
    See also: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#inbox
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
@permission_classes([IsAdminUser|IsAuthenticated&PermittedForRemote])
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
@permission_classes([IsAdminUser|IsAuthenticated&PermittedForRemote])
def PostLikeView(request, author_id, post_id):
    """
    API endpoint that allows users to be viewed or edited.
    """
    post_likes_paginated = []
    object = "http://127.0.0.1:5454/authors/"+ author_id+ "/posts/"+ post_id + "/"  # XXX: Is it really necessary to copy all this other code just so we can also handle the trailing '/'? Also, I think the spec doesn't have a trailing '/' for this endpoint.
    post_likes_object = LikeModel.objects.filter(object=object)
    for likes in post_likes_object:
        serialized_object = LikeSerializer(likes)
        post_likes_paginated.append(serialized_object.data)
    output = {"object": object, "likes": post_likes_paginated}
    return JsonResponse(output, status = 200)



@api_view(['GET'])
@permission_classes([IsAdminUser|IsAuthenticated&PermittedForRemote])
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
@permission_classes([IsAdminUser|IsAuthenticated&PermittedForRemote])
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
