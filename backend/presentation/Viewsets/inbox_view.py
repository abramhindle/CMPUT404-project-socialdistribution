from presentation.models import Inbox, Post, Author
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
        author_id = getAuthorIDFromRequestURL(request, self.kwargs['author_id'])
        inbox = Inbox.objects.get(author=author_id)
        inbox.items.append(request.data)
        inbox.save()
        return Response("Inbox updated successfully", 204)

    def delete(self, request, *args, **kwargs):
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        inbox = get_object_or_404(Inbox, author=author_id)

        inbox.items.clear()
        inbox.save() 
        return Response(status=status.HTTP_204_NO_CONTENT)
