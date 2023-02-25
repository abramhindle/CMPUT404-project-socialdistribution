from rest_framework import serializers
from service.serializers.likes import LikesSerializer
from service.models.liked import Liked

class LikedSerializer(serializers.ModelSerializer):
    items = LikesSerializer(many=True)

    class Meta:
        model = Liked
        fields = ("items",)