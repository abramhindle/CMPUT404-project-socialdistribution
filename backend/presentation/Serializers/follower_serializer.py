from rest_framework import serializers
from presentation.models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['type', 'owner', 'items']
