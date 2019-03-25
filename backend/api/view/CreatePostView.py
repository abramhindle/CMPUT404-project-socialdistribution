from rest_framework import generics, permissions, status
from django.db import transaction
from rest_framework.response import Response
from ..models import Category, Post, AllowToView, ServerUser
from ..serializers import PostSerializer
import uuid
import requests
import json
from .Util import *

class CreatePostView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)
    mutable_keys = ["title", "source", "description", "contentType",
                    "content", "categories", "published", "visibility", "visibleTo", "unlisted"]

    def insert_categories(self, request):
        input_category_list = request.data["categories"]
        for category in input_category_list:
            if (not Category.objects.filter(name=category).exists()):
                Category.objects.create(name=category)

    def insert_author_visibility(self, request):
        visible_to_list = request.data["visibleTo"]

        if (len(visible_to_list) > 0 and request.data.get("visibility") != "PRIVATE"):
            raise ValueError("Error: Post must be private if visibleTo is provided")
        # todo: check if user belongs to other server
        for author in visible_to_list:
            author_profile_id = author.split("/")[-1]
            if (not AuthorProfile.objects.filter(id=author_profile_id).exists()):
                raise ValueError("Error: User in visibleTo does not exist")
            if (not AllowToView.objects.filter(user_id=author).exists()):
                AllowToView.objects.create(user_id=author)

    def insert_post(self, request, user):
        try:
            with transaction.atomic():
                if ("categories" in request.data.keys() and len(request.data["categories"]) > 0):
                    self.insert_categories(request)
                else:
                    raise ValueError("Categories must be provided")

                if ("visibleTo" in request.data.keys()):
                    self.insert_author_visibility(request)
        except ValueError as error:
            return Response(str(error), status.HTTP_400_BAD_REQUEST)

        post_id = uuid.uuid4()
        source_origin_value = "{}api/posts/{}".format(settings.BACKEND_URL, str(post_id))

        request.data["source"] = source_origin_value
        request.data["origin"] = source_origin_value

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.is_valid():
                serializer.save(id=post_id, author=self.request.user.authorprofile)
                return Response("Create Post Success", status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def get_public_posts(self, request):
        public_posts = []
        local_author = AuthorProfile.objects.filter(user=request.user).exists()
        if(local_author):
            print("local author")
            print(ServerUser.objects.all())
            for server_obj in ServerUser.objects.all():
                print("inside loop")
                server_host = server_obj.host
                headers = {'Content-type': 'application/json'}
                url = server_obj.host + "api/posts"
                my_cross_server_username = settings.USERNAME
                my_cross_server_password = settings.PASSWORD
                response = requests.get(url, auth=(my_cross_server_username, my_cross_server_password),
                                        headers=headers)

                if response.status_code != 200:
                    return Response("Cross Server get post Request Fail", status.HTTP_400_BAD_REQUEST)
                else:
                    response_json = json.loads(response.content)
                    public_posts += response_json["posts"]

            # query_set = Post.objects.filter(visibility="PUBLIC", unlisted=False).order_by("-published")
            # public_posts +=  PostSerializer(query_set, many=True).data
            # sorted_public_foreign_posts = sorted(public_posts, key=lambda k: k['published'], reverse=True)

            # response_data = {
            #     "query": "posts",
            #     "count": len(sorted_public_foreign_posts),
            #     "posts": sorted_public_foreign_posts
            # }
            # return Response(response_data, status.HTTP_200_OK)
        # else:
        #     for server_obj in ServerUser.objects.all():
        #         server_host = server_obj.host
        #         headers = {'Content-type': 'application/json'}
        #         url = server_obj.host + "api/posts"
        #         my_cross_server_username = settings.USERNAME
        #         my_cross_server_password = settings.PASSWORD
        #         response = requests.get(url, auth=(my_cross_server_username, my_cross_server_password),
        #                                 headers=headers)
        #         if response.status_code != 200:
        #             return Response("Cross Server get post Request Fail", status.HTTP_400_BAD_REQUEST)
        #         else:
        #             response_json = json.loads(response.content)
        #             public_posts += response_json["posts"]

        query_set = Post.objects.filter(visibility="PUBLIC", unlisted=False).order_by("-published")
        public_posts +=  PostSerializer(query_set, many=True).data
        sorted_public_foreign_posts = sorted(public_posts, key=lambda k: k['published'], reverse=True)

        response_data = {
            "query": "posts",
            "count": len(sorted_public_foreign_posts),
            "posts": sorted_public_foreign_posts
        }
        return Response(response_data, status.HTTP_200_OK)

    def get_public_post_by_id(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            serialized_post = PostSerializer(post).data
            user_profile = AuthorProfile.objects.get(user=request.user)
            request_user_full_id = get_author_id(user_profile, False)
            if(can_read(request_user_full_id, serialized_post)):
                response_data = {
                    "query": "posts",
                    "count": 1,
                    "posts": [serialized_post]
                }
                return Response(response_data, status.HTTP_200_OK)
            else:
                return Response("Error: You do not have permission to view this post", status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Error: Post Does Not Exist", status.HTTP_400_BAD_REQUEST)

    def get(self, request, postid):
        if(postid == ""):
            print("getting public posts")
            return self.get_public_posts(request)
        else:
            return self.get_public_post_by_id(request, postid)

    def post(self, request, *args, **kwargs):
        return self.insert_post(request, request.user)

    @transaction.atomic()
    def put(self, request, postid):
        if (postid == ""):
            return self.insert_post(request, request.user)

        else:
            post_id = self.kwargs['postid']
            try:
                post_to_update = Post.objects.get(id=post_id)
                if (not (request.user.authorprofile.id == post_to_update.author.id)):
                    return Response("Error: You do not have permission to update", status.HTTP_400_BAD_REQUEST)

                if "categories" in request.data.keys():
                    self.insert_categories(request)

                if ("visibleTo" in request.data.keys()):
                    self.insert_author_visibility(request)

                for key, value in request.data.items():
                    if key in self.mutable_keys:
                        if(key == "categories"):
                            post_to_update.categories.set(value)
                        elif(key == "visibleTo"):
                            post_to_update.visibleTo.set(value)
                        else:
                            setattr(post_to_update, key, value)
                    else:
                        raise ValueError("Error: Cannot update field!")

                post_to_update.save()
                return Response("Success: Successfully updated the post", status.HTTP_200_OK)

            except Post.DoesNotExist:
                return Response("Error: This post does not exist!", status.HTTP_400_BAD_REQUEST)
            except ValueError as error:
                return Response(str(error), status.HTTP_400_BAD_REQUEST)

    def delete(self, request, postid=""):
        if (postid == ""):
            return Response("Error: Post ID is Missing", status.HTTP_400_BAD_REQUEST)
        post_id = self.kwargs["postid"]
        try:
            post = Post.objects.get(id=post_id)
            if (request.user.authorprofile.id != post.author.id):
                return Response("Error: Invalid Author", status.HTTP_400_BAD_REQUEST)

            Post.objects.filter(id=post_id).delete()
            return Response("Delete Post Success", status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response("Error: Post Does Not Exist", status.HTTP_400_BAD_REQUEST)
