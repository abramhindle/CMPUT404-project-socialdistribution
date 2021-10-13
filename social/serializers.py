from rest_framework import serializers
from .models import Author, Post, Comment, Follower

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('id','host','displayName','url','github')

class FollowerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Follower
        fields = ('id', 'followers')
