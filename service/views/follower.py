from django.http import *
from service.models.author import Author
from service.service_constants import *
from django.views import View
import json
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView


@method_decorator(csrf_exempt, name='dispatch')
class FollowersAPI(APIView):
    """ GET an Author's all followers """

    http_method_names = ['get']

    def get(self, request, author_id):

        author = Author.objects.get(_id = author_id)

        followers_list = list()

        for follower in list(author.followers.all().order_by('displayName')):
            followers_list.append(follower.toJSON())

        followers_json = encode_Follower_list(followers_list)
        return HttpResponse(json.dumps(followers_json), content_type = CONTENT_TYPE_JSON)
        
@method_decorator(csrf_exempt, name='dispatch')
class FollowerAPI(View):
    """ GET if is a follower PUT a new follower DELETE an existing follower"""
    http_method_names = ['get', 'put', 'delete']
    
    def delete(self, request, author_id, foreign_author_id):
        author = Author.objects.get(_id=author_id)
        foreign_author = Author.objects.get(_id=foreign_author_id)

        author.followers.remove(foreign_author)
        author.save()

        return HttpResponse(status=200)

    def put(self, request, author_id, foreign_author_id):
        #if request.user.is_authenticated:

        if author_id == foreign_author_id:
            return HttpResponseBadRequest() #can't follow yourself!

        author = Author.objects.get(_id = author_id)
        follower = Author.objects.get(_id = foreign_author_id)

        try:
            author.followers.get(_id=foreign_author_id)
        except ObjectDoesNotExist:
            author.followers.add(follower)
            author.save()

            return HttpResponse(status=200)

        return HttpResponse(status=409)

    def get(self, request, author_id, foreign_author_id):
        author = Author.objects.get(_id=author_id)
        foreign = Author.objects.get(_id=foreign_author_id)

        try:
            follower = author.followers.get(_id=foreign._id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        
        follower_json = follower.toJSON()
        return HttpResponse(json.dumps(follower_json), content_type = CONTENT_TYPE_JSON)
        

def encode_Follower_list(authors):
    return {
        "type": "followers",
        "items": authors
    }