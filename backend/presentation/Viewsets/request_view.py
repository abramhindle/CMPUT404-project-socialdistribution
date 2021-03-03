from presentation.models import Author, Follower, Request, Inbox
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from presentation.Serializers.request_serializer import RequestSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
import uuid
from urllib.parse import urlparse

'''
URL: ://service/author/{AUTHOR_ID}/posts/{POST_ID}
GET get the public post
POST update the post (must be authenticated)
DELETE remove the post
PUT create a post with that post_id

Creation URL ://service/author/{AUTHOR_ID}/posts/
GET get recent posts of author (paginated)
POST create a new post but generate a post_id

Be aware that Posts can be images that need base64 decoding.
posts can also hyperlink to images that are public
'''


def getAuthorIDFromRequestURL(request, id):
    parsed_url = urlparse(request.build_absolute_uri())
    host = '{url.scheme}://{url.hostname}:{url.port}'.format(
        url=parsed_url)
    author_id = f"{host}/author/{id}"
    return author_id


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    queryset = Request.objects.all()

    
    # POST a request, sent to the other one's inbox
    # URL: ://service/author/{AUTHOR_ID}/inbox/    
    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        actor_id = request_data.get('actor',None)
        object_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        object_ = Author.objects.get(id=object_id)
        summary = request_data.get('summary', None)
        # add actor as one of object's follower
        followers = get_object_or_404(Follower, owner=object_)
        followers.items.append(actor_id)
        followers.save()
        # send to followers' inboxes
        req_data = {'summary': summary, 'actor': actor_id, 'object': object_id}
        inbox = Inbox.objects.get(author=object_)
        inbox.items.append(req_data)
        inbox.save()

        serializer = self.serializer_class(data=req_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, 200)

