import json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import *
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from service.models.author import Author
from service.service_constants import *
from service.services import team_14, team_22


@method_decorator(csrf_exempt, name='dispatch')
class FollowersAPI(APIView):
    """ GET an Author's all followers """

    http_method_names = ['get']

    def get(self, request, author_id):

        author = Author.objects.get(_id=author_id)

        # reach out and get followers for an author that isn't our own

        # remote-user-t14
        if author.host == settings.REMOTE_USERS[0][1]:
            #team_14.get_multiple_posts(author)

            pass

        # remote-user-t22
        if author.host == settings.REMOTE_USERS[1][1]:
            #team_22.get_multiple_posts(author)

            pass

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
        if author_id == foreign_author_id:
            return HttpResponseBadRequest()  # can't follow yourself!

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
        return HttpResponse(json.dumps(follower_json), content_type=CONTENT_TYPE_JSON)
        

def encode_Follower_list(authors):
    return {
        "type": "followers",
        "items": authors
    }