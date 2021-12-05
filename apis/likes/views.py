from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from apps.posts.models import Comment, Like, Post
from apps.posts.serializers import LikeSerializer
from socialdistribution.utils import Utils
from rest_framework import status

# Create your views here.

def create_like(sender_id, sender_displayName, object_id, host):
    comment_id = Utils.getCommentId(object_id)
    post_id = Utils.getPostId(object_id)
    if comment_id:
        comment = Utils.getCommentDict(comment_id, host)
        if comment == None:
            return None
        comment_id = Utils.cleanCommentId(object_id, host)
    elif (post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except:
            return None
    
    if (not comment_id and not post_id):
        return None

    sender_id = Utils.cleanAuthorId(sender_id, host)
    like = Like.objects.create(author_id=sender_id)

    if (comment_id):
        like.comment_id = comment_id
        like.summary = sender_displayName + " likes your comment"
    elif (post_id):
        like.post_id = post_id
        like.summary = sender_displayName + " likes your post"
    else:
        return None

    like.save()
    return like

def limiter_one_like(host, data_object, sender_id):
    check_postid = Utils.getPostId(data_object)
    check_commentid = Utils.getCommentId(data_object)
    check_authorid = Utils.getAuthorId(sender_id)

    try:
        # Find like with either one of the ids
        # Assuming one of post_id/comment_id is None
        Like.objects.get(post_id=check_postid, comment_id=check_commentid, author_id=check_authorid)

        return Response(status=status.HTTP_204_NO_CONTENT)
    except Like.DoesNotExist as e:
        # Continue as normal
        pass

    return False


class inbox_like(GenericAPIView):
    def post(self, request: HttpRequest, author_id: str):
        """
        Provides Http responses to POST requests that query these forms of URL

        127.0.0.1:8000/author/<author-id>/inbox

        Validates author-id and send a like object to author having author-id =<author-id>

        args:
            - request: a request to get an Author
            - author_id: uuid of the requested author
        returns:
            - HtppResponse containing author data in JSON format if found
            - else HttpResponseNotFound is returned

        """
        host = Utils.getRequestHost(request)
        recipient: dict = Utils.getAuthorDict(author_id, host)

        if (recipient):
            data = JSONParser().parse(request.data) if request.data is str else request.data

            if (not data.__contains__("object")):
                return HttpResponseBadRequest("Body must contain the id of the object being liked")

            if not (data.__contains__("author") and data["author"] and data["author"].__contains__("id")):
                return HttpResponseBadRequest("Body must contain the author who liked this object, and the author's id")

            sender: dict = Utils.getAuthorDict(data["author"]["id"], host)
            if (sender == None):
                return HttpResponseNotFound()

            # Check if one like already exists, return 204 if so
            limited_response = limiter_one_like(host, data["object"], sender["url"])
            if (limited_response):
                return limited_response

            like = create_like(sender["id"], sender["displayName"], data["object"], host)
            if (like == None):
                return HttpResponseNotFound()

            serializer = LikeSerializer(like, context={'host': host})
            formatted_data = Utils.formatResponse(query_type="POST like on inbox", data=serializer.data)
            return Response(formatted_data, status=status.HTTP_201_CREATED)
        else:
            return HttpResponseNotFound()


class post_likes(GenericAPIView):
    def get(self, request: HttpRequest, author_id: str, post_id: str):
        """
        Provides Http responses to GET requests that query these forms of URL

        127.0.0.1:8000/author/<author-id>/post/<post-id>/likes

        Validates author-id and retrieves a list of likes from other authors on author_id’s
        post post_id

        """
        post: Post = None
        try:
            post: Post = Post.objects.get(pk=post_id)
        except:
            return HttpResponseNotFound()

        if (not post or not post.author_id or str(post.author_id) != author_id):
            return HttpResponseNotFound()

        host = request.scheme + "://" + request.get_host()
        likes = Like.objects.filter(post=post_id)
        serializer = LikeSerializer(likes, context={'host': host}, many=True)
        data = {
            "type": "likes",
            # TODO Vova: changed that to match data spec? not sure if it will effect anything
            "data": serializer.data
        }
        return JsonResponse(data)


class comment_likes(GenericAPIView):
    def get(self, request: HttpRequest, author_id: str, post_id: str, comment_id: str):
        """
        Provides Http responses to GET requests that query these forms of URL

        127.0.0.1:8000/author/<author-id>/post/<post-id>/comments/<comment-id>/likes

        Retrieves a list of likes from other authors on author_id’s post post_id comment comment_id
        """
        host = Utils.getRequestHost(request)
        author_id = Utils.cleanAuthorId(author_id, host)

        comment: Comment = None
        try:
            comment: Comment = Comment.objects.get(pk=comment_id)
        except:
            return HttpResponseNotFound()

        if (not comment or str(comment.post_id) != post_id or not comment.post or str(comment.post.author_id) != author_id):
            return HttpResponseNotFound()

        likes = Like.objects.filter(comment_id=comment_id)
        serializer = LikeSerializer(likes, context={'host': host}, many=True)
        data = {
            "type": "likes",
            # TODO Vova: changed that to match data spec? not sure if it will effect anything
            "data": serializer.data
        }
        return JsonResponse(data)


class author_liked(GenericAPIView):
    def get(self, request: HttpRequest, author_id: str):
        """
        Provides Http responses to GET requests that query these forms of URL

        127.0.0.1:8000/author/<author-id>/liked

        Retrieves a list of what public things author with author_id liked.
        """
        host = Utils.getRequestHost(request)
        try:
            likes = Like.objects.filter(author=author_id)
            serializer = LikeSerializer(likes, context={'host': host}, many=True)
            data = {
                "type": "liked",
                # TODO Vova: changed that to match data spec? not sure if it will effect anything
                "data": serializer.data
            }
            return JsonResponse(data)
        except:
            raise Http404

# Examples of calling api
# author uuid(replace): "4f890507-ad2d-48e2-bb40-163e71114c27"
# sending author uuid(replace): "9f48208f-372a-45e6-a024-2b9750c9b494"
# post uuid(replace): "d57bbd0e-185c-4964-9e2e-d5bb3c02841a"
# comment uuid(replace): "a44bacba-c92e-4bf3-a616-aa352cbd1cda"
# Authentication admin(replace): "YWRtaW46YWRtaW4=" (admin:admin)

# POST like to inbox for post !!Please note the trailing / in the url below !!
# curl http://localhost:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/inbox/ -H "Content-Type: application/json" -H "Authorization: Basic YWRtaW46YWRtaW4=" -d '{
# "object":"http://localhost:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/post/d57bbd0e-185c-4964-9e2e-d5bb3c02841a",
# "author": { "type": "author", "id": "9f48208f-372a-45e6-a024-2b9750c9b494" }
# }'

# POST like to inbox for comment !!Please note the trailing / in the url below !!
# curl http://localhost:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/inbox/ -H "Content-Type: application/json" -H "Authorization: Basic YWRtaW46YWRtaW4=" -d '{
# "object":"http://localhost:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/post/d57bbd0e-185c-4964-9e2e-d5bb3c02841a/comments/a44bacba-c92e-4bf3-a616-aa352cbd1cda"
# }'

# GET likes for a post
# curl http://localhost:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/post/d57bbd0e-185c-4964-9e2e-d5bb3c02841a/likes

# GET likes for a comment
# curl http://localhost:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/post/d57bbd0e-185c-4964-9e2e-d5bb3c02841a/comments/a44bacba-c92e-4bf3-a616-aa352cbd1cda/likes

# GET things liked by an author
# curl http://localhost:8000/author/9f48208f-372a-45e6-a024-2b9750c9b494/liked