from presentation.models import Author, Follower, Post, Comment, Likes, Inbox, Liked
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from presentation.Serializers.likes_serializer import LikesSerializer
from rest_framework import viewsets, status
from django.http import JsonResponse
from rest_framework.response import Response
import uuid
from urllib.parse import urlparse
from . import urlutil

def getAuthorIDFromRequestURL(request, id):
    host = urlutil.getSafeURL(request.build_absolute_uri())
    author_id = f"{host}/author/{id}"
    return author_id



class LikesViewSet(viewsets.ModelViewSet):
    serializer_class = LikesSerializer
    queryset = Likes.objects.all()

    def list(self, request, *args, **kwargs):
       
        request_data = request.data.copy()
        liked_author_url = request.build_absolute_uri()
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        _object = liked_author_url[:-7]

        if "comment" in _object:
            comment = _object
            likes = Likes.objects.filter(comment_object=comment)
            likes = list(likes.values())
            return JsonResponse(likes,safe=False)
            
        else:
            post =  _object
            likes = Likes.objects.filter(post_object=post)
            likes = list(likes.values())     
            return JsonResponse(likes,safe=False)

    
    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        context = request_data.get('context',None)
        
        summary = request_data.get('summary',None)
        actor_id = request_data.get('actor',None)
        object_id = request_data.get('object',None)
        

        if "comment" in object_id:
            likes_data = {'type': 'Like','context':context,'summary': summary, 'author':actor_id,'comment_object':object_id}
        else:
            likes_data = {'type': 'Like', 'context':context,'summary': summary, 'author':actor_id,'post_object':object_id}
        '''TODO Liked is not used in user story, so comment these part. If need, just get it out to a new part'''
        # liked = Liked.objects.get(author=actor_id)
        # likes_data['type'] = 'Like'
        # liked.items.append(likes_data)
        # liked.save()

        serializer = self.serializer_class(data=likes_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, 200)