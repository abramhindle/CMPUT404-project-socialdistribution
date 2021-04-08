from presentation.models import Author, Follower, Request, Inbox
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from presentation.Serializers.request_serializer import RequestSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
import uuid
from urllib.parse import urlparse
from . import urlutil
from . import URL

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
        # object_ = Author.objects.get(id=object_id)
        # actor_ = Author.objects.get(id=actor_id)
        followers = Follower.objects.get(owner=object_id)
        if actor_id in followers.items:
            return Response("Already following.", 409)
        try:
            req = Request.objects.get(actor=actor_id, object=object_id)
            print("request already exists!")
        except Request.DoesNotExist:
            r = Request(actor=actor_id, summary=summary, object=object_id)
            r.save()
        # send to followers' inboxes
            request_d = RequestSerializer(r, many=False).data
            inbox = Inbox.objects.get(author=object_id)
            inbox.items.append(request_d)
            inbox.save()
            return Response("success", 200)
        return Response("This request already exists!", 409)

    def delete(self, request, *args, **kwargs):
        request_data = request.data.copy()
        remote = request_data.get('remote', None)
        if remote:
            actor_id = URL.remoteDomain + "/author/" + self.kwargs['actor_id']
        else:
            actor_id = getObjectIDFromRequestURL(
            request, self.kwargs['actor_id'])
        object_id = getObjectIDFromRequestURL(
            request, self.kwargs['object_id'])
        inbox = Inbox.objects.get(author=object_id)
        position = -1
        for i in range(len(inbox.items)):
            if inbox.items[i]["type"] == "follow":
                if (inbox.items[i]["actor"] == actor_id) and (inbox.items[i]["object"] == object_id):
                    position = i
        if position != -1:
            inbox.items.remove(inbox.items[position])
            inbox.save()
            return Response("Delete successful")
        else:
            return Response("No such request. Deletion fails.", 500)
            