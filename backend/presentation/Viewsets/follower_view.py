from presentation.models import Follower, Author
from django.shortcuts import get_object_or_404
from presentation.Serializers.follower_serializer import FollowerSerializer
from presentation.Serializers.author_serializer import AuthorSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from urllib.parse import urlparse
from . import urlutil
from . import URL

'''
URL: ://service/author/{AUTHOR_ID}/followers
    GET: get a list of authors who are their followers
URL: ://service/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    DELETE: remove a follower
    PUT: Add a follower (must be authenticated)
    GET check if follower
'''


def getAuthorIDFromRequestURL(request, id):
    host = urlutil.getSafeURL(request.build_absolute_uri())
    author_id = f"{host}/author/{id}"
    return author_id


class FollowerViewSet(viewsets.ModelViewSet):
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
    # lookup_field = 'author'

    def list(self, request, *args, **kwargs):
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        # author = get_object_or_404(Author, id=author_id)
        queryset = Follower.objects.filter(owner=author_id)
        if queryset.exists():
            followers = Follower.objects.get(owner=author_id)
            return Response({
                'type': 'followers',
                'items': followers.items
            })
        else:
            Follower.objects.create(owner=author_id)
            return Response({
                'type': 'followers',
                'items': []
            })

    def retrieve(self, request, *args, **kwargs):
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        # author = get_object_or_404(Author, id=author_id)
        follower_id = getAuthorIDFromRequestURL(
            request, self.kwargs['foreign_author_id'])
        followers = get_object_or_404(Follower, owner=author_id)
        if follower_id in followers.items:
            f = get_object_or_404(Author, id=follower_id)
            return Response({'exist': True})
        else:
            return Response({'exist': False}, 404)

    def put(self, request, *args, **kwargs):
        request_data = request.data.copy()
        remote = request_data.get('remote', None)
        if remote:
            new_f_id = URL.remoteDomain + "/author/" + self.kwargs['foreign_author_id']
        else: 
            new_f_id = getAuthorIDFromRequestURL(
            request, self.kwargs['foreign_author_id'])
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        # author = get_object_or_404(Author, id=author_id)
        followers = get_object_or_404(Follower, owner=author_id)
        # new_follower = get_object_or_404(Author, id=new_f_id)

        if new_f_id in followers.items:
            return Response("Follower exists already.", 500)
        else:
            followers.items.append(new_f_id)
        followers.save()
        return Response("Follower is successfully added.", 204)

    def delete(self, request, *args, **kwargs):
        request_data = request.data.copy()
        remote = request_data.get('remote', None)
        if remote:
            follower_id = URL.remoteDomain + "/author/" + self.kwargs['foreign_author_id']
        else: 
            follower_id = getAuthorIDFromRequestURL(
            request, self.kwargs['foreign_author_id'])
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        # author = get_object_or_404(Author, id=author_id)
        followers = get_object_or_404(Follower, owner=author_id)
        try:
            followers.items.remove(follower_id)
            followers.save()
        except ValueError:
            return Response("No such a follower. Deletion fails.", 500)
        return Response("Delete successful")
