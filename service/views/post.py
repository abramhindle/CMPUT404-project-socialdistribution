import json
from datetime import datetime, timezone

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from service.models.author import Author
from service.models.post import Post, Category
from service.service_constants import *
from service.services.rest_service import RestService
from django.conf import settings

import requests

# endpoints with just author_id
@method_decorator(csrf_exempt, name='dispatch')
class PostCreation(APIView, RestService):
    http_method_names = ['get', 'post']

    def get(self, request: HttpRequest, *args, **kwargs): # get all recent posts for author_id
        author_id = kwargs['author_id']
        try:
            author = Author.objects.get(_id=author_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        page = request.GET.get('page', '')
        size = request.GET.get('size', '')

        posts = list()

        posts_json = dict()

        # LOCAL author
        if author.host == settings.DOMAIN:
            post_queryset = Post.objects.all().filter(author=author_id).order_by('-published') # only get posts from author_id in the URL, order by the published date
            paged_posts = Paginator(post_queryset, size or 5) # default to size 5

            try:
                page = paged_posts.page(page or 1) # default to page 1
            except:
                page = list()

            for post in page:
                posts.append(post.toJSON())

            posts_json = encode_list(posts)

        # remote-user-t14
        if author.host == settings.REMOTE_USERS[0][1]:
            url = settings.REMOTE_USERS[0][1] + "service/authors/" + author.url.rsplit('/', 1)[-1] + "/posts/"

            response = requests.get(url, auth=settings.REMOTE_USERS[0][2])
            response.close()

            items = list()

            for item in response.json()["items"]:
                post = handle_t14_post(item, author, author.host)
                items.append(post.toJSON())

            posts_json = encode_list(items)

        return HttpResponse(json.dumps(posts_json), content_type=CONTENT_TYPE_JSON)

    def post(self, request: HttpRequest, *args, **kwargs): #create a new post
        if request.content_type != CONTENT_TYPE_JSON:
            return HttpResponseBadRequest()
        
        body = request.data

        author_id = kwargs['author_id']

        post = Post()

        try:
            author = Author.objects.get(_id=author_id)
        except:
            return HttpResponseNotFound()

        post.author = author

        try:
            post._id = Post.create_post_id(author_id)
            post.author = author
            post.title = body["title"]
            post.content = body["content"]
            post.description = body["description"]
            post.source = request.build_absolute_uri() # use the local server ast he source and origin, since this is a BRAND NEW post
            post.origin = request.build_absolute_uri()

            is_valid = self.valid_choice(body["contentType"], Post.CONTENT_TYPES) # we might not need this, but good to have just in case

            if not is_valid:
                return HttpResponseBadRequest()

            post.contentType = body["contentType"]

            categories = create_categories(body["categories"])

            post.published = datetime.now(timezone.utc)

            # TODO: this should be handled by some sort of enum system
            is_valid = self.valid_choice(body["visibility"], Post.VISIBILITY_CHOICES)

            if not is_valid:
                return HttpResponseBadRequest()

            post.visibility = body["visibility"]
            post.unlisted = body["unlisted"]

        except KeyError as error:
            return HttpResponseBadRequest()

        post.save()

        # need to do this here since postgres looks for the post id in the post table before it can add the relation

        for item in categories:
            post.categories.add(item)

        post_json = post.toJSON()

        return HttpResponse(json.dumps(post_json), status=201, content_type = CONTENT_TYPE_JSON)


# endpoints with post_id and author_id
@method_decorator(csrf_exempt, name='dispatch')
class PostWithId(APIView, RestService):
    http_method_names = ['get', 'post', 'delete', 'put']

    def get(self, request: HttpRequest, *args, **kwargs):
        post_id = kwargs["post_id"]
        author_id = kwargs["author_id"]  # TODO: check author_id against current user

        try:
            post = Post.objects.get(_id=post_id)
        except:
            return HttpResponseNotFound()

        post_json = post.toJSON()

        return HttpResponse(json.dumps(post_json), content_type = CONTENT_TYPE_JSON)

    def post(self, request: HttpRequest, *args, **kwargs):
        if request.content_type != CONTENT_TYPE_JSON:
            return HttpResponseBadRequest()

        body = request.data

        post_id = kwargs["post_id"]
        author_id = kwargs["author_id"]

        try:
            post = Post.objects.get(_id=post_id)
        except:
            return HttpResponseNotFound()

        try:
            post.title = body["title"]
            post.content = body["content"]
            post.description = body["description"]

            is_valid = self.valid_choice(body["contentType"], Post.CONTENT_TYPES)  # we might not need this, but good to have just in case

            if not is_valid:
                return HttpResponseBadRequest()

            post.contentType = body["contentType"]

            is_valid = self.valid_choice(body["visibility"], Post.VISIBILITY_CHOICES)  # we might not need this, but good to have just in case

            if not is_valid:
                return HttpResponseBadRequest()

            post.visibility = body["visibility"]

            categories = create_categories(body["categories"])
            
            post.unlisted = bool(body["unlisted"])

        except KeyError as error:
            return HttpResponseBadRequest()  # should probably include the error

        post.save()

        for item in categories:
            post.categories.add(item)

        post_json = post.toJSON()

        return HttpResponse(json.dumps(post_json), status=201, content_type=CONTENT_TYPE_JSON)

    #DELETE
    def delete(self, request: HttpRequest, *args, **kwargs):
        post_id = kwargs["post_id"]
        author_id = kwargs["author_id"]

        try:
            post = Post.objects.get(_id=post_id)
        except:
            return HttpResponseNotFound()

        if post.author._id != author_id: # cannot delete a post for an author that didn't write it
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

def handle_t14_post(post_json, author, hostname):
    # use source as the id for the remote
    # use origin as the host name
    remote_source = hostname + str(post_json["id"]) #this is an int

    print(remote_source)

    try:
        # update old -> don't change host_url or id
        old_post = Post.objects.get(source=remote_source)

        return old_post

    except ObjectDoesNotExist:
        # create new
        new_post = Post().toObject(post_json)
        new_post._id = Post.create_post_id(author._id)
        new_post.categories.set(post_json["categories"])
        new_post.source = remote_source
        new_post.author = author
        new_post.save()

        return new_post
