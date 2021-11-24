from django.db import models
from rest_framework import serializers
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
        nodes = Node.objects.all()
        for node in nodes:
            response = requests.get(node.host_url + "authors/")
            try:
                #print("Response")
                #print(response.status_code)
                #print(response.json())
                #print(node.host_url + "authors")
                authors = response.json()["items"]
                serializer = AuthorSerializer(data=authors, many=True, context={"node": node})
                if serializer.is_valid():
                    serializer.save()
                #else:
                    #print(serializer.error_messages)
            except Exception as e:
                print("Exception:")
                print(e)
                continue