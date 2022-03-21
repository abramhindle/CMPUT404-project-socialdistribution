from rest_framework import serializers
from .models import Following, Follower
from authors.serializers import AuthorSerializer


class FollowerSerializer(serializers.ModelSerializer):
    object = AuthorSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = "__all__"


class FollowingSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Following
        fields = "__all__"
