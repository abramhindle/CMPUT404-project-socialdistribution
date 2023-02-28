from django.http import *
from service.models.author import Author
from service.models.follow import Followers
from service.service_constants import *
from django.views import View
import json
from djongo.models import Q
from django.urls import reverse


class FollowersAPI(View):
    """ GET an Author's all followers """

    http_method_names = ['get']

    def get(self, request,pk):

        Author_Followers = Followers.objects.filter(author___id = pk)
        followerList = list()

        for follower in Author_Followers:
           followerList.append(encode_json(follower.follower))

        followers_json = encode_Follower_list(followerList)
        return HttpResponse(json.dumps(followers_json), content_type = CONTENT_TYPE_JSON)

        

class FollowerAPI(View):
    """ GET if is a follower PUT a new follower DELETE an existing follower"""
    http_method_names = ['get','put','delete']
    
    def delete(self,request,pk,foreignPk):  
        selectedFollowObject = Followers.objects.filter(Q(author___id=pk)&Q(follower___id = foreignPk))
        selectedFollowObject.delete()
        return HttpResponse(status=200)

    def put(self,request,pk,foreignPk):
        
        #if request.user.is_authenticated:
        followedBy = Author.objects.get(_id = foreignPk)
        followTo = Author.objects.get(_id = pk)
        newFollow  = Followers(author = followTo,follower = followedBy)
        newFollow.save()
        return HttpResponse(status=200)

        #else:
            #return HttpResponseRedirect(reverse("getfollowers"),status=303)


    def get(self,request,pk,foreignPk):
        
        selectedFollowObject = Followers.objects.filter(Q(author___id=pk)&Q(follower___id = foreignPk))

        if selectedFollowObject.exists():
        
            selectedFollower = Author.objects.filter(_id = foreignPk)
            follower_json = encode_json(selectedFollower[0])

            return HttpResponse(json.dumps(follower_json), content_type = CONTENT_TYPE_JSON)

        else:
            return HttpResponse(status=404)

def encode_json(author: Author):
    return {
            "type": "author",
            "id": str(author._id),
            "host": author.host,
            "displayName": author.displayName,
            "url": f"{author.host}/authors/{author._id}", #generated here
            "github": author.github,
            "profileImage": author.profileImage,
    }

        
def encode_Follower_list(authors):
    return {
        "type": "followers",
        "items": authors
    }