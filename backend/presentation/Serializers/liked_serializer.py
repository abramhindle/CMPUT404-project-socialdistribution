from rest_framework import serializers
from presentation.models import Liked


class LikedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liked
        fields = ['type','author','items']