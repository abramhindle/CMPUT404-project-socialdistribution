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
        print(request_data)
        actor_id = request_data.get('actor', None)
        object_id = request_data.get('object', None)
        summary = request_data.get('summary', None)
        object_ = Author.objects.get(id=object_id)
        actor_ = Author.objects.get(id=actor_id)
        print('1')
        # add actor as one of object's follower
        #followers = get_object_or_404(Follower, owner=object_)
        print('2')
        #followers.items.append(actor_id)
        #followers.save()
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

    def delete(self, request, *args, **kwargs):
        object_id = getObjectIDFromRequestURL(
            request, self.kwargs['object_id'])
        actor_id = getObjectIDFromRequestURL(
            request, self.kwargs['actor_id'])
        print("actor_id = ", actor_id)
        print("object_id = ", object_id)
        object_ = Author.objects.get(id=object_id)
        actor_ = Author.objects.get(id=actor_id)
        inbox = Inbox.objects.get(author=object_)
        r = get_object_or_404(Request, actor=actor_, object=object_);
        request_d = RequestSerializer(r, many=False).data
        try:
            inbox.items.remove(request_d)
            inbox.save()
            r.delete()
        except ValueError:
            return Response("No such request. Deletion fails.", 500)
        return Response("Delete successful")
