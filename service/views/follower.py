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
from service.services import team_14, team_22, team_16
from rest_framework.permissions import IsAuthenticated

from service.services.team_16 import team_16 as team_16_followers
from service.services.team_10 import followers as team_10_followers


@method_decorator(csrf_exempt, name='dispatch')
class FollowersAPI(APIView):
    """ GET followers for an author """
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, author_id):

        try:
            author = Author.objects.get(_id=author_id, is_active=True)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        # reach out and get followers for an author that isn't our own

        followers_list = list()

        # remote-user-t14
        if author.host == settings.REMOTE_USERS[0][1]:
            #team_14.get_multiple_posts(author)
            pass

        # remote-user-t22
        elif author.host == settings.REMOTE_USERS[1][1]:
            #team_22.get_multiple_posts(author)
            pass

        # remote-user-t16
        elif author.host == settings.REMOTE_USERS[2][1]:
            followers_list = team_16_followers.get_followers(author)

        # remote-user-t10
        elif author.host == settings.REMOTE_USERS[3][1]:
            followers_list = team_10_followers.get_followers(author)

        else:
            for follower in list(author.followers.all().order_by('displayName')):
                followers_list.append(follower.toJSON())

        followers_json = encode_Follower_list(followers_list)
        return HttpResponse(json.dumps(followers_json), content_type = CONTENT_TYPE_JSON)

class Follower_API(APIView):
    """  """
    permission_classes = [IsAuthenticated]   
    http_method_names = ['get']
    def get(self, request, author_id):
        authors = Author.objects.filter(is_active=True).order_by('displayName')
        followers = list()

        for author in authors:
            for follower in list(author.followers.all().order_by('displayName')):
                if follower._id == author_id:
                    followers.append(author.toJSON())

        followers_json = encode_Follower_list(followers)

        return HttpResponse(json.dumps(followers_json), content_type = CONTENT_TYPE_JSON)


class FollowerAPI(APIView):
    """ GET if is a follower PUT a new follower DELETE an existing follower"""
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'delete']

    # TODO: this should remove the foreign author from the author, not the other way
    def delete(self, request, author_id, foreign_author_id):
        author = Author.objects.get(_id=author_id, is_active=True)
        foreign_author = Author.objects.get(_id=foreign_author_id, is_active=True)

        foreign_author.followers.remove(author)
        foreign_author.save()

        return HttpResponse(status=204)

    def put(self, request, author_id, foreign_author_id):
        if author_id == foreign_author_id:
            return HttpResponseBadRequest()  # can't follow yourself!

        # try and get both author and follower
        try:
            author = Author.objects.get(_id = author_id, is_active=True)
            follower = Author.objects.get(_id = foreign_author_id, is_active=True)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        try:
            author.followers.get(_id=foreign_author_id)
        except ObjectDoesNotExist:
            author.followers.add(follower)
            author.save()

            return HttpResponse(status=200)

        return HttpResponse(status=409)

    def get(self, request, author_id, foreign_author_id):
        try:
            author = Author.objects.get(_id = author_id, is_active=True)
            follower = Author.objects.get(_id = foreign_author_id, is_active=True)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        try:
            follower = author.followers.get(_id=follower._id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        
        follower_json = follower.toJSON()
        return HttpResponse(json.dumps(follower_json), content_type=CONTENT_TYPE_JSON)

@method_decorator(csrf_exempt, name='dispatch')
class FriendAPI(View):
      # for friend page
      permission_classes = [IsAuthenticated]
      http_method_names = ['get']

      def get(self, request, author_id): 
        authors = Author.objects.filter(is_active=True).order_by('displayName')
        followers = list()
        for author in authors:
            for follower in list(author.followers.all().order_by('displayName')):
                if follower._id == author_id:
                    followers.append(author.toJSON())

        author = Author.objects.get(_id = author_id, is_active=True)
        followed = list()
        for follower in list(author.followers.all().order_by('displayName')):
            followed.append(follower.toJSON())
        
        friends = list()
        for person in followers:
            if person in followed:
                friends.append(person)


        friends_json = encode_Follower_list(friends)
        return HttpResponse(json.dumps(friends_json), content_type = CONTENT_TYPE_JSON)

def encode_Follower_list(authors):
    return {
        "type": "followers",
        "items": authors
    }