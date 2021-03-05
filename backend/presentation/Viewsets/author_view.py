from presentation.models import Author, Inbox
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from presentation.Serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
import uuid
from urllib.parse import urlparse
from rest_framework.renderers import TemplateHTMLRenderer

'''
URL: ://service/author/{AUTHOR_ID}/
GET: retrieve their profile
POST: update profile
'''

'''
Manual Test:
POST:
{"displayName": "Lara Croft","github": "http://github.com/laracroft","username":"LaraCroft","email": "lara@gmail.com","password": "lara1234"}

'''


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    # GET ://service/author/{AUTHOR_ID}/
    def retrieve(self, request, *args, **kwargs):
        author_id = request.build_absolute_uri()[:-1]
        queryset = Author.objects.get(id=author_id)
        serializer = AuthorSerializer(queryset)
        return Response(serializer.data)

    # POST ://service/author/
    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        # create author
        display_name = request_data.get('displayName', None)
        github = request_data.get('github', None)
        # create id
        auuid = str(uuid.uuid4().hex)
        parsed_url = urlparse(request.build_absolute_uri())
        host = '{url.scheme}://{url.hostname}:{url.port}'.format(
            url=parsed_url)
        author_id = f"{host}/author/{auuid}"
        url = author_id
        author_data = {'id': author_id, 'host': host, 'url': url,
                       'displayName': display_name, 'github': github}
        # create user if given enough information
        username = request_data.get('username', None)
        email = request_data.get('email', None)
        password = request_data.get('password', None)
        if (username and password):
            try:
                user = User.objects.create_user(username, email, password)
                author_data['user'] = user.pk
                serializer = self.serializer_class(data=author_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                # create inbox for the new author
                inbox = InboxSerializer(data={'author': serializer.data["id"]})
                inbox.is_valid(raise_exception=True)
                inbox.save()
                # create liked for the new author
                liked = LikedSerializer(data={'author': serializer.data["id"]})
                liked.is_valid(raise_exception=True)
                liked.save()
                # followers
                followers = FollowerSerializer(
                    data={'owner': serializer.data["id"]})
                followers.is_valid(raise_exception=True)
                followers.save()

                return Response(serializer.data, 200)
            except:
                return Response({'msg': f'{username} exists.'}, 200)
        return Response("Error", 500)

    # PUT ://service/author/{AUTHOR_ID}/
    def update(self, request, *args, **kwargs):
        request_data = request.data.copy()
        #author_id = request_data.get('id', None)
        author_id = request.build_absolute_uri()[:-1]
        author = Author.objects.get(id=author_id)
        new_name = request_data.get('displayName', None)
        new_github = request_data.get('github', None)
        if (new_name):
            author.displayName = new_name
        if (new_github):
            author.github = new_github
        author.save()
        return Response("Author updated successfully", 204)
