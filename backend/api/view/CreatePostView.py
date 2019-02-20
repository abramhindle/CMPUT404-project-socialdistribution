from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Category
from ..serializers import PostSerializer
from django.http import QueryDict
from rest_framework import mixins
import json
import requests
import ast
from pprint import pprint


class CreatePostView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)
    test_list = []

    def insert_post(self, request, user):
        # print(request, "save me")
        input_category_list = request.getlist("categories")
        self.test_list.append(request)
  
        # print(request.data, "save me")
        for category in input_category_list:
            if (not Category.objects.filter(name=category).exists()):
                Category.objects.create(name=category)

        serializer = PostSerializer(data=request)
        # print(serializer)
        if serializer.is_valid():
            # print("am i valid")
            serializer.save(author=user.authorprofile)
            return Response("Create Post Success", status.HTTP_200_OK)
        else:
            # print("or am i not valid")
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        # print(request.user, "post user")
        print("\n",request.data, "dreaming")
        return self.insert_post(request.data, request.user)

    def put(self, request, postid):
        # print(request, "put boi")
        # print(request.body)
        # print(QueryDict(request.body))
        # print(request.user, "save me fam")
        # print("nani")
        print("I am PUT")
        pprint(vars(request))
        print(request._data)
        # if (len(postid) < 1):
            
            # responseData = QueryDict(request.body)
            # print(request.data, "hello")
            # request_body = request.body.decode("utf-8")

            # print("\n",request_body)
            # content_list = request_body[1:-1].split(",")
            # request_data = QueryDict()
            # query_dict_arg = ""
            # print(content_list)z
            # print(json.loads(request_body))
            # print(request_body)

            # request_body = request_body.replace("'", '"')
            # request_body = request_body[1:-1]
            # print(request_body)
            # data = json.loads(request_body)
            # print(data)
            # hello = ast.literal_eval(request_body)
            # print(hello)
            # query_dict_param = ""
            # for key, value in hello.items():
            #     if (not (isinstance(value, str))):
            #         value = str(value)
            #     query_dict_param = query_dict_param + key + "=" + value + "&"
            
            # Q = QueryDict(query_dict_param[0:-1])
            # print(Q)
            # return self.insert_post(Q, request.user)
        return Response("yay Success", status.HTTP_200_OK)
