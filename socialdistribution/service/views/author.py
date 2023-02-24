from django.http import *
from service.models.author import Author,Followers
from service.service_constants import *
from django.views import View

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json

from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from djongo.models import Q
from django.urls import reverse

# Create your views here.

class MultipleAuthors(View):
    http_method_names = ["get"]
    
    def get(self, request, *args, **kwargs):
        authors_queryset = Author.objects.all().order_by('displayName')
        page = request.GET.get('page', '')
        size = request.GET.get('size', '')

        if not page or not size:
            return HttpResponseBadRequest()

        paged_authors = Paginator(authors_queryset, size)

        try:
            page = paged_authors.page(page)
        except:
            page = list()
        
        authors = list()

        for author in page:
            authors.append(encode_json(author))

        authors = encode_list(authors)

        return HttpResponse(json.dumps(authors), content_type = CONTENT_TYPE_JSON)

class SingleAuthor(View):
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        self.id = kwargs['id']
        try: 
            author = Author.objects.get(_id=self.id)
        except:
            author = None

        if not author:
            return HttpResponseNotFound()

        author_json = encode_json(author)

        return HttpResponse(json.dumps(author_json), content_type = CONTENT_TYPE_JSON)

    def post(self, request, *args, **kwargs):
        body = request.body.decode(UTF8)
        body = json.loads(body)

        self.id = kwargs['id']

        try:
            author = Author.objects.get(_id=self.id)
        except:
            return HttpResponseNotFound()

        if "displayName" in body:
            author.displayName = body["displayName"]

        if "github" in body:
            author.github = body["github"]

        if "profileImage" in body:
            author.profileImage = body["profileImage"]

        author.save() #updates whatever is set in the above if statements

        author_json = encode_json(author)

        return HttpResponse(json.dumps(author_json), status=202, content_type = CONTENT_TYPE_JSON)

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

def encode_list(authors):
    return {
        "type": "author",
        "items": authors
    }


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
        
        if request.user.is_authenticated:
            followedBy = Author.objects.get(_id = foreignPk)
            followTo = Author.objects.get(_id = pk)
            newFollow  = Followers(author = followTo,follower = followedBy)
            newFollow.save()
            return HttpResponse(status=200)

        else:
            return HttpResponseRedirect(reverse("getfollowers"),status=303)


    def get(self,request,pk,foreignPk):
        
        selectedFollowObject = Followers.objects.filter(Q(author___id=pk)&Q(follower___id = foreignPk))

        if selectedFollowObject.exists():
        
            selectedFollower = Author.objects.filter(_id = foreignPk)
            follower_json = encode_json(selectedFollower[0])

            return HttpResponse(json.dumps(follower_json), content_type = CONTENT_TYPE_JSON)

        else:
            return HttpResponse(status=404)


        
def encode_Follower_list(authors):
    return {
        "type": "followers",
        "items": authors
    }