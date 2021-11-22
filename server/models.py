from django.db import models
from rest_framework import serializers
from author.models import Author
from author.serializers import AuthorSerializer
import requests

class Setting(models.Model):
    allow_user_sign_up = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Setting, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def user_sign_up_enabled(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj.allow_user_sign_up

class Node(models.Model):
    # If there is a prefix it will be included in the host_url
    host_url = models.URLField()
    # The credentials we need to use to connect to the node
    username = models.TextField()
    password = models.TextField()

    @staticmethod
    def update_authors():
        for node in Node.objects.all():
            response = requests.get(node.host_url + "authors", auth=(node.username, node.password))
            authors = response.json()["items"]
            serializer = AuthorSerializer(data=authors, many=True)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.error_messages)