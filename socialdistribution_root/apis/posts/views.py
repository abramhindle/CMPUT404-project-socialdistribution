# Using serializers and Rest framework:
# https://www.django-rest-framework.org/tutorial/3-class-based-views/

from django.http import JsonResponse, Http404
from django.http.request import HttpRequest

from apps.posts.models import Post
from apps.core.models import User
from apps.posts.serializers import PostSerializer

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status

# TODO work with permissions and allowed scope

# Used for formatting and styling responses
def compose_posts_dict(query_type, data):
    json_result = {
        'query': query_type,
        'data': data
    }

    return json_result


class post(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    # GET get the public post
    def get(self, request: HttpRequest, author_id: str, post_id: str, format=None):
        post = self.get_object(post_id)
        serializer = PostSerializer(post)
        formatted_data = compose_posts_dict(query_type="GET on post", data=serializer.data)

        return Response(formatted_data)

    # POST update the post (must be authenticated)
    def post(self, request: HttpRequest, author_id: str, post_id: str):
        post = self.get_object(post_id)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # set uri post id for json response
            post = self.get_object(post_id)
            post.set_post_id(request.get_host())
            post.save()

            # serialize saved post for response
            serializer = PostSerializer(post)
            formatted_data = compose_posts_dict(query_type="POST on post", data=serializer.data)

            return Response(formatted_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT create a post with that post_id
    def put(self, request: HttpRequest, author_id: str, post_id: str, format=None):
        user: User = User.objects.get(pk=author_id)

        if (user):
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                post = Post.objects.create(
                        id=post_id,
                        author=user, 
                        **serializer.validated_data
                    )
                # set uri post id for json response
                post.set_post_id(request.get_host())
                post.save()

                # serialize saved post for response
                serializer = PostSerializer(post)
                formatted_data = compose_posts_dict(query_type="PUT on post", data=serializer.data)

                return Response(formatted_data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    # DELETE remove the post
    def delete(self, request: HttpRequest, author_id: str, post_id: str, format=None):
        post = self.get_object(post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class posts(GenericAPIView):
    # This is being used to paginate queryset
    serializer_class = PostSerializer

    # GET get recent posts of author (paginated)
    def get(self, request: HttpRequest, author_id: str):
        user: User = User.objects.get(pk=author_id)

        if (user):
            # filter out only posts by given author and paginate
            queryset = Post.objects.filter(author_id=author_id)
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)

            serializer = self.get_serializer(page, many=True)
            dict_data = compose_posts_dict(query_type="GET on posts", data=serializer.data)
            result = self.get_paginated_response(dict_data)

            return JsonResponse(result.data, safe=False)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # POST create a new post but generate a post_id
    def post(self, request: HttpRequest, author_id: str):
        user: User = User.objects.get(pk=author_id)

        if (user):
            data = JSONParser().parse(request)
            serializer = PostSerializer(data=data)
            if serializer.is_valid():
                post = Post.objects.create(
                    author=user, 
                    **serializer.validated_data
                )
                # set uri post id for json response
                post.set_post_id(request.get_host())
                post.save()

                # serialize saved post for response
                serializer = PostSerializer(post)
                formatted_data = compose_posts_dict(query_type="POST on posts", data=serializer.data)

                return Response(formatted_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # TODO lookup error for unauthorized like here and above
            return Response(status=status.HTTP_400_BAD_REQUEST)
            

# Examples of calling api
# author uuid(replace): "582b3b39-e455-4e7b-88e2-3df2d7d35995"
# post uuid(replace): "f2478e2a-4422-4b6b-abd5-70b5076af6ce"
# user cookie(replace): "IBCSaVWFkMXABVyyBR36GPdKcjaf9rBaVwWx7eQQgFhlQLfzVWSSXZOk7YnDhtzm"
# 2nd post uuid(replace): "f3589e1a-5533-5b7b-abd6-81b6187af7ce"
    # GET post
    # curl http://localhost:8000/author/582b3b39-e455-4e7b-88e2-3df2d7d35995/posts/f2478e2a-4422-4b6b-abd5-70b5076af6ce/ -H "X-CSRFToken: IBCSaVWFkMXABVyyBR36GPdKcjaf9rBaVwWx7eQQgFhlQLfzVWSSXZOk7YnDhtzm" -H "Cookie: csrftoken=IBCSaVWFkMXABVyyBR36GPdKcjaf9rBaVwWx7eQQgFhlQLfzVWSSXZOk7YnDhtzm"
    
    # Put post
    #     curl -X PUT http://localhost:8000/author/582b3b39-e455-4e7b-88e2-3df2d7d35995/posts/f3589e1a-5533-5b7b-abd6-81b6187af7ce/ -H "X-CSRFToken: IBCSaVWFkMXABVyyBR36GPdKcjaf9rBaVwWx7eQQgFhlQLfzVWSSXZOk7YnDhtzm" -H "Cookie: csrftoken=IBCSaVWFkMXABVyyBR36GPdKcjaf9rBaVwWx7eQQgFhlQLfzVWSSXZOk7YnDhtzm" -H "Content-Type: application/json" -d '{
    # "type":"post",
    # "title":"A post posted with put api on /post/",
    # "description":"This post discusses stuff -- brief",
    # "contentType":"text/plain",
    # "author":{
    #       "type":"author",
    #       "id":"582b3b39-e455-4e7b-88e2-3df2d7d35995"
    # },
    # "visibility":"PUBLIC",
    # "unlisted":false}'  

    # POST post
    #     curl -X POST http://localhost:8000/author/582b3b39-e455-4e7b-88e2-3df2d7d35995/posts/f3589e1a-5533-5b7b-abd6-81b6187af7ce/ -H "X-CSRFToken: IBCSaVWFkMXABVyyBR36GPdKcjaf9rBaVwWx7eQQgFhlQLfzVWSSXZOk7YnDhtzm" -H "Cookie: csrftoken=IBCSaVWFkMXABVyyBR36GPdKcjaf9rBaVwWx7eQQgFhlQLfzVWSSXZOk7YnDhtzm" -H "Content-Type: application/json" -d '{
    # "type":"post",
    # "title":"A post that was changed by POST with api /post/"}'  

    # Delete post
    # curl -X DELETE http://localhost:8000/author/582b3b39-e455-4e7b-88e2-3df2d7d35995/posts/f3589e1a-5533-5b7b-abd6-81b6187af7ce/ -H "X-CSRFToken: IBCSaVWFkMXABVyyBR36GPdKcjaf9rBaVwWx7eQQgFhlQLfzVWSSXZOk7YnDhtzm" -H "Cookie: csrftoken=IBCSaVWFkMXABVyyBR36GPdKcjaf9rBaVwWx7eQQgFhlQLfzVWSSXZOk7YnDhtzm"
    # 
    #--------------------------------------------------------------------
    # 
    # GET posts
    # curl http://localhost:8000/author/582b3b39-e455-4e7b-88e2-3df2d7d35995/posts/ -H "X-CSRFToken: IBCSaVWFkMXABVyyBR36GPdKcjaf9rBaVwWx7eQQgFhlQLfzVWSSXZOk7YnDhtzm" -H "Cookie: csrftoken=IBCSaVWFkMXABVyyBR36GPdKcjaf9rBaVwWx7eQQgFhlQLfzVWSSXZOk7YnDhtzm"
    
    #  GET posts with pagination
    #  curl "http://localhost:8000/author/582b3b39-e455-4e7b-88e2-3df2d7d35995/posts/?page=2&size=3"  -H "X-CSRFToken: IBCSaVWFkMXABVyyBR36GPdKcjaf9rBaVwWx7eQQgFhlQLfzVWSSXZOk7YnDhtzm" -H "Cookie: csrftoken=IBCSaVWFkMXABVyyBR36GPdKcjaf9rBaVwWx7eQQgFhlQLfzVWSSXZOk7YnDhtzm"

    # POST posts
    #     curl -X POST http://localhost:8000/author/582b3b39-e455-4e7b-88e2-3df2d7d35995/posts/ -H "X-CSRFToken: IBCSaVWFkMXABVyyBR36GPdKcjaf9rBaVwWx7eQQgFhlQLfzVWSSXZOk7YnDhtzm" -H "Cookie: csrftoken=IBCSaVWFkMXABVyyBR36GPdKcjaf9rBaVwWx7eQQgFhlQLfzVWSSXZOk7YnDhtzm" -H "Content-Type: application/json" -d '{
    # "type":"post",
    # "title":"A post title about a post about web dev",
    # "description":"This post discusses stuff -- brief",
    # "contentType":"text/markdown",
    # "author":{
    #       "type":"author",
    #       "id":"582b3b39-e455-4e7b-88e2-3df2d7d35995"
    # },
    # "visibility":"PUBLIC",
    # "unlisted":false}'     