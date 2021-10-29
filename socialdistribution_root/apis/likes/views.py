from re import search
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from apps.posts.models import Comment, Like, Post
from apps.posts.serializers import LikeSerializer
from socialdistribution.utils import Utils
from rest_framework import status
from apps.core.models import Author

# Create your views here.

class inbox_like(GenericAPIView):
    def post(self, request: HttpRequest, author_id: str):
        recipient: Author = None
        try:
            recipient: Author = Author.objects.get(pk=author_id)
        except:
            return HttpResponseNotFound()

        if (recipient):
            host = request.scheme + "://" + request.get_host()

            data = JSONParser().parse(request)

            if (not data.__contains__("object")):
                HttpResponseBadRequest("Body must contain the id of the object being liked")

            if (not data.__contains__("author") or not data["author"] or not data["author"].__contains__("id")):
                HttpResponseBadRequest("Body must contain the author who liked this object, and the author's id")

            sender: Author = None
            try:
                sender: Author = Author.objects.get(pk=data["author"]["id"])
            except:
                return HttpResponseNotFound()

            comment: Comment = None
            post: Post = None

            res = search('comments/(.*)$', data["object"])
            comment_id = res.group(1) if res else None
            if comment_id:
                try:
                    comment = Comment.objects.get(pk=comment_id)
                except:
                    return HttpResponseNotFound()
            else:
                res = search('post/(.*)$', data["object"])
                post_id = res.group(1) if res else None
                if (post_id):
                    try:
                        post = Post.objects.get(pk=post_id)
                    except:
                        return HttpResponseNotFound()
                        
            like = Like.objects.create(author=sender)

            if (comment):
                like.comment = comment
                like.summary = sender.displayName + " likes your comment"
            elif (post):
                like.post = post
                like.summary = sender.displayName + " likes your post"
            else:
                HttpResponseNotFound()

            like.save()

            serializer = LikeSerializer(like, context={'host': host})
            formatted_data = Utils.formatResponse(query_type="POST like on inbox", data=serializer.data)
            return Response(formatted_data, status=status.HTTP_201_CREATED)
        else:
            return HttpResponseNotFound()

class post_likes(GenericAPIView):
    def get(self, request: HttpRequest, author_id: str, post_id: str):        
        post: Post = None
        try:
            post: Author = Post.objects.get(pk=post_id)
        except:
            return HttpResponseNotFound()

        if (post.id != post_id or not post.author or str(post.author.id) != author_id):
            return HttpResponseNotFound()

        host = request.scheme + "://" + request.get_host()
        likes = Like.objects.filter(post=post_id)
        serializer = LikeSerializer(likes, context={'host': host}, many=True)
        data = {
            "type": "likes",
            "items": serializer.data
        }
        return JsonResponse(data)


class comment_likes(GenericAPIView):
    def get(self, request: HttpRequest, author_id: str, post_id: str, comment_id: str):        
        comment: Comment = None
        try:
            comment: Comment = Post.objects.get(pk=comment_id)
        except:
            return HttpResponseNotFound()

        if (not comment or not comment.post or comment.post.id != post_id or not comment.post.author or str(comment.post.author.id) != author_id):
            return HttpResponseNotFound()

        host = request.scheme + "://" + request.get_host()
        likes = Like.objects.filter(comment_id=comment_id)
        serializer = LikeSerializer(likes, context={'host': host}, many=True)
        data = {
            "type": "likes",
            "items": serializer.data
        }
        return JsonResponse(data)


class author_liked(GenericAPIView):
    def get(self, request: HttpRequest, author_id: str):
        host = request.scheme + "://" + request.get_host()
        likes = Like.objects.filter(author=author_id)
        serializer = LikeSerializer(likes, context={'host': host}, many=True)
        data = {
            "type": "liked",
            "items": serializer.data
        }
        return JsonResponse(data)

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