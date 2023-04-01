from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from service.models.author import Author
from service.models.like import Like
from service.models.post import Post
from rest_framework.permissions import IsAuthenticated

from service.services import team_10
from django.conf import settings


class LikedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, author_id):
        try:
            author_query = Author.objects.get(_id=author_id, is_active=True)
            liked = Like.objects.filter(author=author_query)
        except:
            return Response(status=404)
        
        likes = list()

        for item in liked:
            likes.append(item.toJSON())

        return Response(encode_list(likes))
    

class LikesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, author_id, post_id):

        try:
            author = Author.objects.get(_id=author_id)
        except ObjectDoesNotExist:
            return Response({"error": "No author exists!"}, status=404)

        try:
            post = Post.objects.get(_id=post_id)
        except ObjectDoesNotExist:
            return Response({"error": "No post exists!"}, status=404)

        json_likes = list()

        if post.origin == settings.REMOTE_USERS[0][1]:
            #team_14.get_multiple_posts(author)
            pass
        # remote-user-t22
        elif post.origin == settings.REMOTE_USERS[1][1]:
            #team_22.get_multiple_posts(author)
            pass
        # remote-user-t16
        elif post.origin == settings.REMOTE_USERS[2][1]:
            #team_16.(author, page, size)
            pass

        elif post.origin == settings.REMOTE_USERS[3][1]:
            json_likes = team_10.get_likes(author, post)

        else:
            post_likes = list(Like.objects.filter(object=post_id).all())

            for like in post_likes:
                json_likes.append(like.toJSON())

        return Response(encode_list(json_likes), status=200)

def encode_list(likes):
    return {
        "type": "liked",
        "items": likes
    }