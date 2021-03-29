from presentation.models import Author, Follower, Request, Inbox
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from presentation.Serializers.request_serializer import RequestSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
import uuid
from urllib.parse import urlparse
from . import urlutil

'''
This allows someone to follow you, so you can send them your posts.

Sent to inbox
'''
def getObjectIDFromRequestURL(request, id):
    host = urlutil.getSafeURL(request.build_absolute_uri())
    object_id = f"{host}/author/{id}"
    return object_id

class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    queryset = Request.objects.all()

    # POST a request, sent to the other one's inbox
    # URL: ://service/author/{AUTHOR_ID}/inbox/
    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        actor_id = request_data.get('actor', None)
        object_id = request_data.get('object', None)
        if actor_id == object_id:
            return Response("Can't follow yourself!", 409)
        summary = request_data.get('summary', None)
        object_ = Author.objects.get(id=object_id)
        actor_ = Author.objects.get(id=actor_id)
        followers = Follower.objects.get(owner=object_)
        if actor_id in followers.items:
            return Response("Already following.", 409)
        try:
            req = Request.objects.get(actor=actor_, object=object_)
            print("request already exists!")
        except Request.DoesNotExist:
            r = Request(actor=actor_, summary=summary, object=object_)
            r.save()
        # send to followers' inboxes
            request_d = RequestSerializer(r, many=False).data
            inbox = Inbox.objects.get(author=object_)
            inbox.items.append(request_d)
            inbox.save()
            return Response("success", 200)
        return Response("This request already exists!", 409)

    def delete(self, request, *args, **kwargs):
        object_id = getObjectIDFromRequestURL(
            request, self.kwargs['object_id'])
        actor_id = getObjectIDFromRequestURL(
            request, self.kwargs['actor_id'])
        object_ = Author.objects.get(id=object_id)
        actor_ = Author.objects.get(id=actor_id)
        inbox = Inbox.objects.get(author=object_)
        r = get_object_or_404(Request, actor=actor_, object=object_)
        request_d = RequestSerializer(r, many=False).data
        try:
            inbox.items.remove(request_d)
            inbox.save()
            r.delete()
        except ValueError:
            return Response("No such request. Deletion fails.", 500)
        return Response("Delete successful")
