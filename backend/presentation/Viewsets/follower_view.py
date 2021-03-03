from presentation.models import Follower, Author
from django.shortcuts import get_object_or_404
from presentation.Serializers.follower_serializer import FollowerSerializer
from presentation.Serializers.author_serializer import AuthorSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from urllib.parse import urlparse

'''
URL: ://service/author/{AUTHOR_ID}/followers
    GET: get a list of authors who are their followers
URL: ://service/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    DELETE: remove a follower
    PUT: Add a follower (must be authenticated)
    GET check if follower
'''


def getAuthorIDFromRequestURL(request, id):
    parsed_url = urlparse(request.build_absolute_uri())
    host = '{url.scheme}://{url.hostname}:{url.port}'.format(
        url=parsed_url)
    author_id = f"{host}/author/{id}"
    return author_id


class FollowerViewSet(viewsets.ModelViewSet):
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
    # lookup_field = 'author'

    def list(self, request, *args, **kwargs):
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        author = get_object_or_404(Author, id=author_id)
        queryset = Follower.objects.filter(owner=author)
        if queryset.exists():
            followers = Follower.objects.get(owner=author)
            return Response({
                'type': 'followers',
                'items': followers.items
            })
        else:
            Follower.objects.create(owner=author)
            return Response({
                'type': 'followers',
                'items': []
            })

    def retrieve(self, request, *args, **kwargs):
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        author = get_object_or_404(Author, id=author_id)
        follower_id = getAuthorIDFromRequestURL(
            request, self.kwargs['foreign_author_id'])
        followers = get_object_or_404(Follower, owner=author)
        if follower_id in followers.items:
            f = get_object_or_404(Author, id=follower_id)
            return Response({'exist': True})
        else:
            return Response({'exist': False}, 404)

    def put(self, request, *args, **kwargs):
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        author = get_object_or_404(Author, id=author_id)
        followers = get_object_or_404(Follower, owner=author)

        new_f_id = getAuthorIDFromRequestURL(
            request, self.kwargs['foreign_author_id'])
        new_follower = get_object_or_404(Author, id=new_f_id)

        if new_follower in followers.items:
            return Response("Follower exists already.", 500)
        else:
            followers.items.append(new_f_id)
        followers.save()
        return Response("Follower is successfully added.", 204)

    def delete(self, request, *args, **kwargs):
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        author = get_object_or_404(Author, id=author_id)
        followers = get_object_or_404(Follower, owner=author)

        follower_id = getAuthorIDFromRequestURL(
            request, self.kwargs['foreign_author_id'])
        try:
            followers.items.remove(follower_id)
            followers.save()
        except ValueError:
            return Response("No such a follower. Deletion fails.", 500)
        return Response("Delete successful")
