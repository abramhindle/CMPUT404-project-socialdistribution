# Implementation of serializers from the tutorial: https://www.django-rest-framework.org/tutorial/1-serialization/

from rest_framework import serializers
from apps.core.models import User

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="get_post_id", read_only=True)
    type = serializers.CharField(default="author", read_only=True)

    class Meta:
        model = User
        fields = [
            'type', 
            'id', 
            'displayName',
            'github',
            'profileImage'
        ]