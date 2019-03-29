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
            for server_obj in ServerUser.objects.all():
                headers = {'Content-type': 'application/json'}
                try:
                    url = "{}{}posts".format(server_obj.host, server_obj.prefix)
                    response = requests.get(url,
                                            auth=(server_obj.send_username, server_obj.send_password),
                                            headers=headers)

                    if response.status_code != 200:
                        return Response(response.json(), status.HTTP_400_BAD_REQUEST)
                    else:
                        response_json = json.loads(response.content)
                        public_posts += response_json["posts"]

                except Exception as e:
                    return Response(e,status.HTTP_400_BAD_REQUEST)

        query_set = Post.objects.filter(visibility="PUBLIC", unlisted=False).order_by("-published")
        public_posts +=  PostSerializer(query_set, many=True).data
        sorted_public_foreign_posts = sorted(public_posts, key=lambda k: k['published'], reverse=True)
        return_posts = []
        for post in sorted_public_foreign_posts:
            comments = []
            for comment in post["comments"]:
                parsed_post_url = urlparse(comment["author"])
                commenter_host = '{}://{}/'.format(parsed_post_url.scheme, parsed_post_url.netloc)
                local_author = AuthorProfile.objects.filter(user=request.user)
                if local_author.exists():
                    local_author = local_author[0]
                    author = AuthorProfileSerializer(local_author).data
                    comment["author"] = author
                    comments.append(comment)  

                elif not local_author.exists():
                    # send request to other server
                    # to verify the profile
                    try:
                        server_obj = ServerUser.objects.get(host=commenter_host)
                        commenter_short_id = get_author_id(comment["author"]["id"])
                        url = "{}api/author/{}".format(server_obj.host, commenter_short_id)
                        response = requests.post(url,
                                                auth=(server_obj.send_username, server_obj.send_password),
                                                headers=headers,
                                                data=json.dumps(request.data)
                                                )
                        # return Response(response.json(), response.status_code)
                        if(response.status != 200):
                            return Response("Error: Unable to get foreign profile", status.HTTP_400_BAD_REQUEST)
                        
                        else:
                            response_json = json.loads(response.content)
                            comment["author"] = response_json["author"]
                            comments.append(comment)
                    except ServerUser.DoesNotExist:
                        return Response("Error: Author not from allowed host", status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        return Response(e,status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Error: Unable to provide comments", status.HTTP_400_BAD_REQUEST)
  
            post["comments"] = comments
            return_posts.append(post)

        response_data = {
            "query": "posts",
            "count": len(sorted_public_foreign_posts),
            "posts": return_posts
        }
        return Response(response_data, status.HTTP_200_OK)


    def get_public_post_by_id(self, request, post_id):
        author_exist = AuthorProfile.objects.filter(user=request.user).exists()
        server_user_exist = ServerUser.objects.filter(user=request.user).exists()

        if not (author_exist or server_user_exist):
            return Response("Invalid request user", status.HTTP_400_BAD_REQUEST)

        # from front end
        if author_exist:
            is_local_uuid = True
            # for foreign post:
            # expect front end to send http://127.0.0.1:8000/api/posts/http%3A%2F%2F127.0.0.1%3A1234%2Fapi%2Fposts%2F163974c0-b350-4e9b-a708-b570acee826d
            # for local post:
            # expect front end to send http://127.0.0.1:8000/api/posts/163974c0-b350-4e9b-a708-b570acee826d
            try:
                uuid.UUID(post_id)
            except ValueError:
                is_local_uuid = False

            if is_local_uuid:
                try:
                    user_profile = AuthorProfile.objects.get(user=request.user)
                    authorId = get_author_id(user_profile, False)
                except AuthorProfile.DoesNotExist:
                    return Response("Error: Author does not exist", status.HTTP_400_BAD_REQUEST)

            # front end requesting foreign post
            else:
                try:
                    parsed_url = urlparse(post_id)
                    foreign_host = '{}://{}/'.format(parsed_url.scheme, parsed_url.netloc)
                    post_short_id = post_id.split("/")[-1]
                    server_user = ServerUser.objects.get(host=foreign_host)
                    user_profile = AuthorProfile.objects.get(user=request.user)
                    headers = {'Content-type': 'application/json',
                               "X-Request-User-ID": AuthorProfileSerializer(user_profile).data["id"]}
                    url = "{}{}posts/{}".format(server_user.host, server_user.prefix, post_short_id)
                    response = requests.get(url, auth=(server_user.send_username, server_user.send_password),
                                            headers=headers)

                    return Response(response.json(), response.status_code)
                except Exception as e:
                    return Response(e, status.HTTP_400_BAD_REQUEST)
        # when server make the request
        elif server_user_exist:
            try:
                authorId = request.META["HTTP_X_REQUEST_USER_ID"]
            except:
                return Response("Error: X-Request-User-ID header missing", status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Error: Request not from valid server", status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(id=post_id)
            serialized_post = PostSerializer(post).data
            sorted_comments= sorted(serialized_post["comments"], key=lambda k: k['published'], reverse=True)
            serialized_post["comments"] = sorted_comments
            comments = []
            for comment in serialized_post["comments"]:
                parsed_post_url = urlparse(comment["author"])
                commenter_host = '{}://{}/'.format(parsed_post_url.scheme, parsed_post_url.netloc)
                local_author = AuthorProfile.objects.filter(user=request.user)
                if local_author.exists():
                    local_author = local_author[0]
                    author = AuthorProfileSerializer(local_author).data
                    comment["author"] = author
                    comments.append(comment)
                elif not local_author.exists():
                    # send request to other server
                    # to verify the profile
                    try:
                        server_obj = ServerUser.objects.get(host=commenter_host)
                        commenter_short_id = get_author_id(comment["author"]["id"])
                        url = "{}api/author/{}".format(server_obj.host, commenter_short_id)
                        response = requests.post(url,
                                                auth=(server_obj.send_username, server_obj.send_password),
                                                headers=headers,
                                                data=json.dumps(request.data)
                                                )
                        # return Response(response.json(), response.status_code)
                        if(response.status != 200):
                            return Response("Error: Unable to get foreign profile", status.HTTP_400_BAD_REQUEST)
                        
                        else:
                            response_json = json.loads(response.content)
                            comment["author"] = response_json["author"]
                            comments.append(comment)
                    except ServerUser.DoesNotExist:
                        return Response("Error: Author not from allowed host", status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        return Response(e,status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Error: Unable to provide comments", status.HTTP_400_BAD_REQUEST)

            serialized_post["comments"] = comments
            if(can_read(authorId, serialized_post)):
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
