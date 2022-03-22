from rest_framework import serializers
from liked.models import Liked
import requests as r
from likes.serializers import LikesSerializer


class LikedSerializer(serializers.ModelSerializer):


    item=LikesSerializer(read_only=True)
    object = serializers.URLField()

    class Meta:
        model = Liked
        fields = ["type", "items"]

