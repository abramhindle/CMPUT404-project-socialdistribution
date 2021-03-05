from presentation.models import Author, Follower, Request, Inbox
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from presentation.Serializers.request_serializer import RequestSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
import uuid
from urllib.parse import urlparse

'''
This allows someone to follow you, so you can send them your posts.

Sent to inbox
'''


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    queryset = Request.objects.all()

    # POST a request, sent to the other one's inbox
    # URL: ://service/author/{AUTHOR_ID}/inbox/    
    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        actor_id = request_data.get('actor',None)
        object_id = request_data.get('object', None)
        summary = request_data.get('summary', None)
        object_ = Author.objects.get(id=object_id)
        actor_ = Author.objects.get(id=actor_id)
        # add actor as one of object's follower
        followers = get_object_or_404(Follower, owner=object_)
        followers.items.append(actor_id)
        followers.save()
        r = Request(actor=actor_, summary=summary, object=object_)
        r.save()
        # send to followers' inboxes
        request_d = RequestSerializer(r, many=False).data
        # req_data = {'summary': summary, 'actor': actor_id, 'object': object_id}
        inbox = Inbox.objects.get(author=object_)
        inbox.items.append(request_d)
        inbox.save()
        # serializer = self.serializer_class(data=req_data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response("success", 200)

