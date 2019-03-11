from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client, RequestFactory
from rest_framework.test import RequestsClient
from ..models import Category, Post, AuthorProfile
from ..serializers import PostSerializer
import json
import uuid

class GetPostsTestCase(TestCase):
    client = RequestsClient()
    username = "test123"
    password = "pw123"