# python manage.py test api

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from mixer.backend.django import mixer
import json

from socialDistribution.models import Post, Category
from .test_authors import create_author
from cmput404.constants import HOST, API_PREFIX
from datetime import datetime


def get_post_json(post):
    previousCategories = Category.objects.filter(post=post)
    previousCategoriesNames = [cat.category for cat in previousCategories]
    return {
        "type":"posts",
        "page": None,
        "size": None,
        "items": [{
            "type":"post",
            # title of a post
            "title":post.title,
            # id of the post
            "id": f"http://{HOST}/{API_PREFIX}/author/{post.author.id}/posts/{post.id}",
            # where did you get this post from?
            "source":post.source,
            # where is it actually from
            "origin":post.origin,
            # a brief description of the post
            "description":post.description,
            # The content type of the post
            # assume either
            # text/markdown -- common mark
            # text/plain -- UTF-8
            # application/base64
            # image/png;base64 # this is an embedded png -- images are POSTS. So you might have a user make 2 posts if a post includes an image!
            # image/jpeg;base64 # this is an embedded jpeg
            # for HTML you will want to strip tags before displaying
            "contentType":post.content_type,
            "content":post.content_text, # 
            # the author has an ID where by authors can be disambiguated
            "author":post.author.as_json(),
            # categories this post fits into (a list of strings
            "categories":previousCategoriesNames,
            # comments about the post
            # return a maximum number of comments
            # total number of comments for this post
            "count": post.count,
            # the first page of comments
            "comments":f"http://{HOST}/{API_PREFIX}/author/{post.author.id}/posts/{post.id}/comments/",
            # commentsSrc is OPTIONAL and can be missing
            # You should return ~ 5 comments per post.
            # should be sorted newest(first) to oldest(last)
            # this is to reduce API call counts
            "commentsSrc":post.get_comments_as_json(),
            # ISO 8601 TIMESTAMP
            "published":str(post.pub_date),
            # visibility ["PUBLIC","FRIENDS"]
            "visibility":post.visibility,
            # for visibility PUBLIC means it is open to the wild web
            # FRIENDS means if we're direct friends I can see the post
            # FRIENDS should've already been sent the post so they don't need this
            "unlisted":post.unlisted
            # unlisted means it is public if you know the post name -- use this for images, it's so images don't show up in timelines
        }]
            }

class PostsViewTest(TestCase):

    def test_get_posts_basic(self):
        self.maxDiff = None
        post = mixer.blend(Post, content_type='PL')
        expected = get_post_json(post)

        response = self.client.get(reverse('api:posts', args=(post.author.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected)