from presentation.models import Inbox, Post, Author, Follower
from django.shortcuts import get_object_or_404
from presentation.Serializers.inbox_serializer import InboxSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
import uuid
from urllib.parse import urlparse
from . import urlutil

'''
URL: ://service/author/{AUTHOR_ID}/inbox

GET: if authenticated get a list of posts sent to {AUTHOR_ID}

POST: send a post to the author
    if the type is “post” then add that post to the author’s inbox
    if the type is “follow” then add that follow is added to the author’s inbox to approve later
    if the type is “like” then add that like to the author’s inbox

DELETE: clear the inbox

'''

def getAuthorIDFromRequestURL(request, id):
    host = urlutil.getSafeURL(request.build_absolute_uri())
    author_id = f"{host}/author/{id}"
    return author_id

class InboxViewSet(viewsets.ModelViewSet):
    serializer_class = InboxSerializer

    # get a list of posts sent to {AUTHOR_ID}
    def retrieve(self, request, *args, **kwargs):
        author_id = getAuthorIDFromRequestURL(request, self.kwargs['author_id'])
        queryset = Inbox.objects.filter(author=author_id)
        if queryset.exists():
            posts = Inbox.objects.get(author=author_id)
            return Response({
                'type': 'inbox',
                'author': author_id,
                'items': posts.items
            })
        else:
            Inbox.objects.create(author=author_id)
            return Response({
                'type': 'inbox',
                'author': author_id,
                'items': []
            })

    def update(self, request, *args, **kwargs):
        request_data = request.data.copy()
        author_id = getAuthorIDFromRequestURL(request, self.kwargs['author_id'])
        inbox = Inbox.objects.get(author=author_id)
        # check duplicates
        if request_data in inbox.items:
            return Response("Already exists!", 409)
        objectType = request_data.get('type', None)
        if objectType == 'post':
            inbox.items.append(request_data)
            inbox.save()
            return Response("Inbox updated successfully")
        elif objectType == 'Like':
            actor_id = request_data.get('actor',None)
            object_id = request_data.get('object',None)
            context = request_data.get('context',None)
            summary = request_data.get('summary',None)
            if "comment" in object_id:
                likes_data = {'type': 'Like','context':context,'summary': summary, 'author':actor_id,'comment_object':object_id}
                inbox.items.append(likes_data)
                inbox.save()
            else:
                likes_data = {'type': 'Like', 'context':context,'summary': summary, 'author':actor_id,'post_object':object_id}
                inbox.items.append(likes_data)
                inbox.save()
            return Response("Inbox updated successfully")
        elif objectType == 'follow':
            actor_id = request_data.get('actor', None)
            object_id = request_data.get('object', None)
            if actor_id == object_id:
                return Response("Can't follow yourself!", 409)
            followers = Follower.objects.get(owner=object_id)
            if actor_id in followers.items:
                return Response("Already following.", 409)
            inbox.items.append(request_data)
            inbox.save()
            return Response("Inbox updated successfully")
        else:
            return Response("Wrong Type", 500)

    def delete(self, request, *args, **kwargs):
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        inbox = get_object_or_404(Inbox, author=author_id)

        inbox.items.clear()
        inbox.save() 
        return Response("Delete successful")
