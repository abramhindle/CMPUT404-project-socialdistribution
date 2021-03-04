from presentation.models import Liked, Author
from django.shortcuts import get_object_or_404
from presentation.Serializers.liked_serializer import LikedSerializer
from presentation.Serializers.author_serializer import AuthorSerializer
from rest_framework import viewsets, status
from django.http import JsonResponse
from rest_framework.response import Response
from urllib.parse import urlparse

'''
URL: ://service/author/{author_id}/liked
GET list what public things author_id liked.
It’s a list of of likes originating from this author
'''


def getAuthorIDFromRequestURL(request, id):
    parsed_url = urlparse(request.build_absolute_uri())
    host = '{url.scheme}://{url.hostname}:{url.port}'.format(
        url=parsed_url)
    author_id = f"{host}/author/{id}"
    return author_id


class LikedViewSet(viewsets.ModelViewSet):
    serializer_class = LikedSerializer
    queryset = Liked.objects.all()

    def list(self, request, *args, **kwargs):
        author_id = getAuthorIDFromRequestURL(request, self.kwargs['author_id'])
        author_ = get_object_or_404(Author, id=author_id)
        queryset = Liked.objects.filter(author=author_id)
        if queryset.exists():
            items = Liked.objects.filter(author=author_id)
            for item in items:
                item.id = None
            items = list(items.values())
            return JsonResponse(items,safe=False)

        else:
            Liked.objects.create(author=author_id)
            return Response({
                'type': 'liked',
                'author': author_id,
                'items': []
            })


    def retrieve(self, request, *args, **kwargs):
        author_id = getAuthorIDFromRequestURL(request, self.kwargs['author_id'])
        queryset = Liked.objects.get(author=author_id)
        serializer = LikedViewSet(queryset)
        return Response(serializer.data)