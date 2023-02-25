from django.http import *
from service.models.post import Post, Category
from service.models.author import Author
from service.service_constants import *
from django.views import View
from datetime import datetime, timezone
from service.services.rest_service import RestService

import uuid

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json

from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

#endpoints with just author_id
@method_decorator(csrf_exempt, name='dispatch')
class PostCreation(View, RestService):
    http_method_names = ['get', 'post']

    def get(self, request: HttpRequest, *args, **kwargs): #get all recent posts for author_id
        self.author_id = kwargs['author_id']

        page = request.GET.get('page', '')
        size = request.GET.get('size', '')

        post_queryset = Post.objects.all().filter(author=self.author_id).order_by('-published') #only get posts from author_id in the URL, order by the published date

        paged_posts = Paginator(post_queryset, size or 5) #default to size 5

        try:
            page = paged_posts.page(page or 1) #default to page 1
        except:
            page = list()

        posts = list()

        for post in page:
            posts.append(post.toJSON())

        posts_json = encode_list(posts)

        return HttpResponse(json.dumps(posts_json), content_type = CONTENT_TYPE_JSON)
    
    def post(self, request: HttpRequest, *args, **kwargs): #create a new post
        if request.content_type != CONTENT_TYPE_JSON:
            return HttpResponseBadRequest()
        
        body = request.body.decode(UTF8)
        body = json.loads(body)

        self.author_id = kwargs['author_id']

        post = Post()

        try:
            author = Author.objects.get(_id=self.author_id)
        except:
            return HttpResponseNotFound()

        try:
            post.author = author
            post.title = body["title"]
            post.content = body["content"]
            post.description = body["description"]
            post.source = request.build_absolute_uri() #use the local server ast he source and origin, since this is a BRAND NEW post
            post.origin = request.build_absolute_uri()

            is_valid = self.valid_choice(body["contentType"], Post.CONTENT_TYPES) #we might not need this, but good to have just in case

            if not is_valid:
                return HttpResponseBadRequest()

            post.contentType = body["contentType"]

            categories = create_categories(body["categories"])

            post.categories.set(categories)

            post.published = datetime.now(timezone.utc)

            #this should be handled by some sort of enum system

            is_valid = self.valid_choice(body["visibility"], Post.VISIBILITY_CHOICES)

            if not is_valid:
                return HttpResponseBadRequest()

            post.visibility = body["visibility"]
            post.unlisted = body["unlisted"]

        except KeyError:
            return HttpResponseBadRequest()

        post.save()

        return HttpResponse(status=201)


#Endpoints with post_id and author_id
@method_decorator(csrf_exempt, name='dispatch')
class PostWithId(View, RestService):
    http_method_names = ['get', 'post', 'delete', 'put']

    #GET
    def get(self, request: HttpRequest, *args, **kwargs):
        self.post_id = kwargs["post_id"]
        self.author_id = kwargs["author_id"]

        try:
            post = Post.objects.get(_id=self.post_id)
        except:
            return HttpResponseNotFound()

        post_json = post.toJSON()

        return HttpResponse(json.dumps(post_json), content_type = CONTENT_TYPE_JSON)

    #POST
    def post(self, request: HttpRequest, *args, **kwargs):
        if request.content_type != CONTENT_TYPE_JSON:
            return HttpResponseBadRequest()
        
        body = request.body.decode(UTF8)
        body = json.loads(body)

        self.post_id = kwargs["post_id"]
        self.author_id = kwargs["author_id"]

        try:
            post = Post.objects.get(_id=self.post_id)
        except:
            return HttpResponseNotFound()

        try:
            post.title = body["title"]
            post.content = body["content"]
            post.description = body["description"]

            is_valid = self.valid_choice(body["contentType"], Post.CONTENT_TYPES) #we might not need this, but good to have just in case

            if not is_valid:
                return HttpResponseBadRequest()

            post.contentType = body["contentType"]

            is_valid = self.valid_choice(body["visibility"], Post.VISIBILITY_CHOICES) #we might not need this, but good to have just in case

            if not is_valid:
                return HttpResponseBadRequest()

            post.visibility = body["visibility"]

            categories = create_categories(body["categories"])

            post.categories.set(categories)
            
            post.unlisted = bool(body["unlisted"])

        except KeyError:
            return HttpResponseBadRequest()

        post.save()

        return HttpResponse(status=201)

    #DELETE
    def delete(self, request: HttpRequest, *args, **kwargs):
        self.post_id = kwargs["post_id"]
        self.author_id = kwargs["author_id"]

        try:
            post = Post.objects.get(_id=self.post_id)
        except:
            return HttpResponseNotFound()

        if post.author._id != self.author_id: #cannot delete a post for an author that didn't write it
            return HttpResponseNotFound()

        post.delete()

        return HttpResponse(status=202)

    #PUT
    def put(self, request: HttpRequest, *args, **kwargs):

        return HttpResponse(status=405) # we will do this later, not super useful as a local API without multiple hosts


def create_categories(json_categories):
    categories = []
    for item in json_categories:
        try:
            category = Category.objects.create(data=item)
        except:
            category = Category.objects.get(data=item)
        categories.append(category)
    
    return categories

def encode_list(posts):
    return {
        "type": "posts",
        "items": posts
    }