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
from rest_framework.permissions import IsAuthenticated


@method_decorator(csrf_exempt, name='dispatch')
class FollowersAPI(APIView):
    """ GET an Author's all followers """
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, author_id):

        author = Author.objects.get(_id = author_id, is_active=True)

        followers_list = list()

        for follower in list(author.followers.all().order_by('displayName')):
            followers_list.append(follower.toJSON())

        followers_json = encode_Follower_list(followers_list)
        return HttpResponse(json.dumps(followers_json), content_type = CONTENT_TYPE_JSON)

class Follower_API(APIView):
    # for follower page   
    http_method_names = ['get']
    def get(self, request, author_id):
        authors = Author.objects.all().order_by('displayName')
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
    
    def delete(self, request, author_id, foreign_author_id):
        author = Author.objects.get(_id=author_id, is_active=True)
        foreign_author = Author.objects.get(_id=foreign_author_id, is_active=True)

        foreign_author.followers.remove(author)
        foreign_author.save()

        return HttpResponse(status=204)

    def put(self, request, author_id, foreign_author_id):
        #if request.user.is_authenticated:

        if author_id == foreign_author_id:
            return HttpResponseBadRequest() #can't follow yourself!

        author = Author.objects.get(_id = author_id, is_active=True)
        follower = Author.objects.get(_id = foreign_author_id, is_active=True)

        try:
            author.followers.get(_id=foreign_author_id)
        except ObjectDoesNotExist:
            author.followers.add(follower)
            author.save()

            return HttpResponse(status=200)

        return HttpResponse(status=409)

    def get(self, request, author_id, foreign_author_id):
        author = Author.objects.get(_id=author_id, is_active=True)
        foreign = Author.objects.get(_id=foreign_author_id, is_active=True)

        try:
            follower = author.followers.get(_id=foreign._id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        
        follower_json = follower.toJSON()
        return HttpResponse(json.dumps(follower_json), content_type = CONTENT_TYPE_JSON)

@method_decorator(csrf_exempt, name='dispatch')
class FriendAPI(View):
      # for friend page
      http_method_names = ['get']

      def get(self, request, author_id): 
        authors = Author.objects.all().order_by('displayName')
        followers = list()
        for author in authors:
            for follower in list(author.followers.all().order_by('displayName')):
                if follower._id == author_id:
                    followers.append(author.toJSON())


        author = Author.objects.get(_id = author_id)
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